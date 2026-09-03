# 🌐 Multi-Device Development Guide

Work on **Content Repurposer** from any device: Mac, Windows, Linux, or mobile browser. Choose your workflow.

---

## Option 1: Local Development (Recommended for Heavy Coding)

**Setup:** ~5 minutes on first run

### Mac/Linux
```bash
cd content-repurposer
make setup       # Install Python + Node dependencies
make dev         # Run backend + frontend
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Edit files in VS Code

### Windows (PowerShell)
```bash
cd content-repurposer
python -m venv backend\.venv
backend\.venv\Scripts\activate
pip install -r backend/requirements.txt
cd frontend && npm install
# Then run in two terminals:
# Terminal 1: cd backend && python app.py
# Terminal 2: cd frontend && npm run dev
```

### Switching Devices (Local to Local)
1. On PC #1: `git push`
2. On PC #2: `git pull && make setup && make dev`

---

## Option 2: GitHub Codespaces (Recommended for Switching Devices)

**Setup:** Browser-based, instant, syncs across devices

### Launch Codespace
1. Go to: https://github.com/m2ks79/content-repurposer
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait ~2 min for environment to set up (Makefile runs `make setup` automatically)

### Access
- **VS Code in Browser:** Same experience as desktop VS Code
- **Ports auto-exposed:**
  - Frontend: https://yourname-content-repurposer-5173.preview.app.github.dev
  - Backend: https://yourname-content-repurposer-5000.preview.app.github.dev

### Workflow
1. Edit files in Codespace
2. Run: `make dev` (backend + frontend run)
3. Tests pass? Commit & push
4. Switch to another device → Same Codespace, same state

### Mobile (Phone/Tablet)
- Open Codespace URL in Safari/Chrome
- Use phone's browser keyboard
- Push changes from phone browser → works!

### Cost
- Free for GitHub Pro: 60 core-hours/month
- Sufficient for this project (development only)

---

## Option 3: Docker (Recommended for "Just Works" Setup)

**No local dependencies needed** — Docker handles everything

### Install Docker
- Mac/Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt install docker docker-compose`

### Run
```bash
cd content-repurposer
docker-compose up
```

**Access:**
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- Changes auto-reload (hot module reloading)

### On Any Device
```bash
# Mac: same command
docker-compose up

# Windows: same command
docker-compose up

# Linux: same command
docker-compose up
```

### Teardown
```bash
docker-compose down
```

---

## Option 4: Replit (Quick Public Demo)

**No install needed, share link with anyone**

### Setup
1. Go to [Replit](https://replit.com)
2. Import repo: https://github.com/m2ks79/content-repurposer
3. Click **Run**

### Access
- Instant live URL you can share
- Collaborators can join + edit together
- Code auto-saves to GitHub on commit

### Downside
- Slower than local (for heavy video processing)
- Free tier limits

---

## Option 5: DigitalOcean / Heroku (Cloud Hosting)

**Deploy production version, accessible globally**

### Deploy to Heroku (Free Tier: Stopped)
```bash
heroku create your-app-name
git push heroku main
heroku logs --tail
```

**Then:** https://your-app-name.herokuapp.com

### Deploy to DigitalOcean (Affordable)
```bash
# Requires DigitalOcean account
doctl apps create --spec app.yaml
```

---

## Recommended Workflows by Use Case

### 👨‍💻 Full-Time Development
**Use:** GitHub Codespaces (sync across devices) + Docker (if testing locally)
```bash
# Codespaces: code, test, push
# Then on laptop: git pull && docker-compose up (same state)
```

### 📱 Mobile + Desktop Switching
**Use:** GitHub Codespaces + mobile browser
```bash
# Work on phone: Codespaces browser
# Work on desktop: Codespaces browser or local
# Everything syncs automatically
```

### 🚀 Production Ready
**Use:** Docker + hosted platform
```bash
# Develop locally: `make dev`
# Deploy: `docker-compose up` on cloud server
# Share link: https://app.example.com
```

### 🎓 Learning / Quick Testing
**Use:** Replit or local `make dev`
```bash
# Replit: click Run, instant live
# Local: `make dev`, instant feedback loops
```

---

## Syncing Between Devices

### GitHub Codespaces (Automatic)
- Changes sync in real-time
- Same file state across devices
- **No manual git push needed**

### Local Git (Manual)
```bash
# Device A (finished work)
git add .
git commit -m "Feature: add captions"
git push

# Device B (want to continue)
git pull
make setup  # if dependencies added
make dev
```

### Docker (Image-based)
```bash
# Device A
docker-compose up
# (develop, test, commit)
git push

# Device B
git pull
docker-compose up  # exact same environment
```

---

## Troubleshooting

### "Can't connect to port 5000/5173"
- Check if process running: `lsof -i :5000`
- Kill it: `kill -9 <PID>`
- Restart: `make dev`

### "npm install fails"
```bash
rm -rf frontend/node_modules package-lock.json
npm install
```

### "FFmpeg not found" (video processing)
```bash
# Mac
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### "Python venv issues"
```bash
rm -rf backend/.venv
python -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```

### GitHub Codespaces takes too long to load
- Kill & recreate: Codespaces → ⋯ → Delete
- Create new: fresh, faster environment

---

## Quick Reference

| Scenario | Command | Best For |
|----------|---------|----------|
| Quick test | `make dev` | Local coding |
| Any device | Codespaces | Switching PCs/mobile |
| No install | Docker | "Just works" |
| Public demo | Replit | Sharing early version |
| Production | Cloud deploy | Live product |

---

## Next: Choose Your Setup

1. **GitHub Codespaces** (recommended) — Open: https://github.com/m2ks79/content-repurposer/codespaces
2. **Local** — Run: `make setup && make dev`
3. **Docker** — Run: `docker-compose up`

Pick one, and let's build! 🚀
