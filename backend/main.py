"""
VYNRIX — Lead Engine Backend
FastAPI server → calls Claude API → returns generated website HTML
Deploy on Railway / Render / Fly.io
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import anthropic
import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────
app = FastAPI(title="Vynrix Lead Engine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend build (if exists)
frontend_path = Path("../frontend")
if frontend_path.exists():
    app.mount("/app", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

# ─────────────────────────────────────────────
# ANTHROPIC CLIENT
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

# ─────────────────────────────────────────────
# IN-MEMORY LEAD STORE (replace with DB later)
# ─────────────────────────────────────────────
leads_db: dict = {}

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────
class GenerateRequest(BaseModel):
    name: str
    type: str
    city: str
    phone: str
    description: Optional[str] = ""
    needs: Optional[list] = []

class Lead(BaseModel):
    name: str
    type: str
    city: str
    phone: str
    score: Optional[int] = 75
    status: Optional[str] = "new"

class LeadUpdate(BaseModel):
    status: str

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "project": "Vynrix Lead Engine",
        "status": "running",
        "api_key_set": bool(ANTHROPIC_API_KEY),
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# ── GENERATE WEBSITE ──────────────────────────
@app.post("/api/generate")
async def generate_website(req: GenerateRequest):
    """
    Takes business info + needs → Claude generates full HTML website
    """
    if not client:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set")

    # Build needs list string
    needs_text = ""
    if req.needs:
        needs_text = "\n".join([f"- {n.get('title','')}: {n.get('desc','')}" for n in req.needs])
    else:
        needs_text = "- Professional website with hero, services, contact sections"

    prompt = f"""You are an expert web designer. Create a complete, production-quality single-file HTML website for a local business.

OUTPUT ONLY raw HTML. No markdown. No explanation. No backticks. Start directly with <!DOCTYPE html>

=== BUSINESS BRIEF ===
Name: {req.name}
Type: {req.type}
City: {req.city}, Kerala, India
Phone: {req.phone}
{f'Description: {req.description}' if req.description else ''}

=== WHAT THIS BUSINESS SPECIFICALLY NEEDS ===
{needs_text}

=== DESIGN REQUIREMENTS ===
1. Mobile-first, fully responsive design
2. Beautiful font pair from Google Fonts that perfectly suits a {req.type}
3. Premium color scheme that fits this business type
4. Build ALL the needed sections listed above as real working features
5. Hero section with compelling, specific tagline for this business type
6. Working features: forms with validation, smooth scroll, interactive elements
7. A prominent CTA button "✓ I Want This Website!" with onclick: alert('Thank you! Vynrix will contact you within 24 hours. Cost: ₹8,000–₹15,000')
8. Smooth CSS animations on load (staggered reveals using animation-delay)
9. Footer: "Crafted by Vynrix AI — vynrix.in"
10. Make it look so impressive the owner IMMEDIATELY wants to pay for it

=== CRITICAL ===
- Output ONLY the complete HTML file
- Start with <!DOCTYPE html>
- All CSS and JS inline (no external files except Google Fonts)
- Every section must be fully built — no placeholders"""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )
        html = message.content[0].text

        # Clean any accidental markdown fences
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0].strip()
        elif "```" in html:
            html = html.split("```")[1].split("```")[0].strip()

        return {
            "success": True,
            "html": html,
            "business": req.name,
            "generated_at": datetime.now().isoformat()
        }

    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── LEADS CRUD ────────────────────────────────
@app.get("/api/leads")
def get_leads():
    return {"leads": list(leads_db.values()), "total": len(leads_db)}

@app.post("/api/leads")
def create_lead(lead: Lead):
    lead_id = str(uuid.uuid4())[:8]
    leads_db[lead_id] = {
        "id": lead_id,
        **lead.dict(),
        "created_at": datetime.now().isoformat(),
        "proto_html": ""
    }
    return {"id": lead_id, **leads_db[lead_id]}

@app.patch("/api/leads/{lead_id}")
def update_lead(lead_id: str, update: LeadUpdate):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    leads_db[lead_id]["status"] = update.status
    leads_db[lead_id]["updated_at"] = datetime.now().isoformat()
    return leads_db[lead_id]

@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    del leads_db[lead_id]
    return {"deleted": lead_id}


# ── STATS ─────────────────────────────────────
@app.get("/api/stats")
def get_stats():
    leads = list(leads_db.values())
    return {
        "total": len(leads),
        "hot":      len([l for l in leads if l["status"] == "hot"]),
        "new":      len([l for l in leads if l["status"] == "new"]),
        "accepted": len([l for l in leads if l["status"] == "accepted"]),
        "built":    len([l for l in leads if l.get("proto_html")]),
    }


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
