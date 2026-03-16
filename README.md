# 🚀 Vynrix — AI Lead Engine

> Automatically finds businesses without websites → AI builds a prototype → alerts you when they're interested

[![GitHub](https://img.shields.io/badge/GitHub-Vynrix%2FProject--3-181717?logo=github)](https://github.com/Vynrix/Project-3)
[![Made by](https://img.shields.io/badge/Made%20by-Sreejith%20R-blueviolet)](https://github.com/Vynrix)

---

## 📁 Project Structure

```
vynrix-lead-engine/
├── backend/
│   ├── main.py              # FastAPI server (Claude API calls here)
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Copy to .env and add your key
├── frontend/
│   └── index.html           # Full dashboard (open in browser)
├── .gitignore
├── Procfile                 # For Railway/Render deployment
├── railway.json             # Railway config
├── nixpacks.toml            # Build config
└── README.md
```

---

## ⚡ Quick Start (Local)

### Step 1 — Clone the repo
```bash
git clone https://github.com/Vynrix/Project-3.git
cd Project-3
```

### Step 2 — Setup backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### Step 3 — Add your Anthropic API key
Open `backend/.env` and paste your key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get key from: https://console.anthropic.com

### Step 4 — Run the backend
```bash
python main.py
# Server runs at http://localhost:8000
```

### Step 5 — Open the dashboard
Open `frontend/index.html` in your browser.

The dashboard auto-detects if backend is running at `localhost:8000`.

---

## 🌐 Deploy to Railway (Live URL)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — Vynrix Lead Engine"
git remote add origin https://github.com/Vynrix/Project-3.git
git push -u origin main
```

### Step 2 — Deploy on Railway
1. Go to **railway.app** → Sign up free
2. Click **New Project** → **Deploy from GitHub**
3. Select your `Project-3` repo
4. Railway auto-detects Python and builds it

### Step 3 — Add your API key on Railway
1. In Railway dashboard → your project → **Variables** tab
2. Add: `ANTHROPIC_API_KEY` = `sk-ant-your-key-here`
3. Railway auto-restarts with the key

### Step 4 — Get your live URL
Railway gives you a URL like:
```
https://vynrix-lead-engine-production.up.railway.app
```

### Step 5 — Connect frontend to your live backend
Open `frontend/index.html` → find this line:
```javascript
: '';   // ← After Railway deploy, paste URL here
```
Change it to:
```javascript
: 'https://vynrix-lead-engine-production.up.railway.app';
```

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | `/`             | Health check + API key status |
| GET  | `/health`       | Simple health ping |
| POST | `/api/generate` | Generate website HTML from business info |
| GET  | `/api/leads`    | Get all leads |
| POST | `/api/leads`    | Add a new lead |
| PATCH| `/api/leads/:id`| Update lead status |
| GET  | `/api/stats`    | Pipeline statistics |

### POST /api/generate — Example
```json
{
  "name":  "Malabar Biriyani House",
  "type":  "Restaurant",
  "city":  "Kozhikode",
  "phone": "+91 9876543210",
  "needs": [
    {"title": "Online Menu",    "desc": "Customers check menu before visiting", "p": true},
    {"title": "Table Booking",  "desc": "Reduce phone calls",                   "p": true},
    {"title": "Food Gallery",   "desc": "Photos of dishes increase footfall",   "p": false}
  ]
}
```

---

## 📲 How the Full Flow Works

```
1. Open frontend/index.html
2. Type city + business type → Click "Generate Leads"
3. Leads appear with AI Needs Analysis cards
4. Click any lead → See what features their website needs
5. Click "Build Website" → Claude API generates a real website
6. Preview in Desktop / Tablet / Mobile view
7. Click "Send to Client" → They get a link
8. If they click "I Want This" → You get an alert
9. Click "Accept" → Schedule your call and close the deal 💰
```

---

## 🔧 Termux (Android) Setup

```bash
pkg update && pkg upgrade -y
pkg install python git
pip install fastapi uvicorn anthropic python-dotenv --prefer-binary
git clone https://github.com/Vynrix/Project-3.git
cd Project-3/backend
cp .env.example .env
nano .env   # paste your API key
python main.py
```

---

## 💰 Monetisation Ideas

- Charge ₹8,000–₹25,000 per website from interested businesses
- Monthly retainer for updates: ₹1,500–₹3,000/month
- Add Google Ads management as upsell
- White-label the tool and sell access to other freelancers

---

## 🗺️ Roadmap

- [ ] Real Google Maps Places API integration for lead scraping
- [ ] Email outreach automation (Brevo/Resend)
- [ ] Telegram bot alerts integration
- [ ] Netlify auto-deploy for prototypes
- [ ] CRM with notes per lead
- [ ] Payment integration (Razorpay)

---

## 🛠 Built With

- **Backend**: FastAPI + Python + Anthropic Claude API
- **Frontend**: Vanilla HTML/CSS/JS (no framework — runs anywhere)
- **Deploy**: Railway (backend) + GitHub Pages (frontend)
- **AI**: Claude claude-opus-4-5 for website generation

---

Made with ❤️ by **Sreejith R** · Vynrix
