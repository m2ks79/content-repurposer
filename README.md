# Content Repurposer MVP

Convert ONE video → Platform-optimized versions (TikTok, Instagram Reels, YouTube Shorts, LinkedIn)

**Phase 1:** Basic repurposing (splitting, aspect ratio, format conversion)

## Quick Start

### Local Development

```bash
# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Backend:** http://localhost:5000
**Frontend:** http://localhost:5173

### Cloud Development (GitHub Codespaces)

1. Fork this repo to your GitHub
2. Open in Codespaces
3. Terminal: `make setup` (installs everything)
4. Terminal: `make dev` (runs both backend + frontend)

### Docker

```bash
docker-compose up
# App at http://localhost:5000
```

## Project Structure

```
content-repurposer/
├── backend/               Python FastAPI + video processing
│   ├── app.py
│   ├── requirements.txt
│   └── utils/
│       ├── video_processor.py
│       └── claude_optimizer.py
├── frontend/              React Vite app
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docs/                  Docs & guides
├── docker-compose.yml
├── .env.example
└── README.md
```

## Features (Phase 1)

- ✅ Drag-drop video upload (mp4, mov, webm)
- ✅ Auto-generate platform versions:
  - TikTok (1080x1920, 15-60s, vertical)
  - Instagram Reel (1080x1920, vertical)
  - YouTube Shorts (1080x1920, 15-60s)
  - LinkedIn Video (1080x1080, square)
- ✅ One-click download all versions
- ✅ Basic watermark option

## Roadmap

- **Phase 2:** Smart captions (AI-generated per platform)
- **Phase 3:** Scheduling + publishing integration
- **Phase 4:** Analytics + performance tracking
- **Phase 5:** Team collaboration

## API Docs

See `/docs/API.md` for endpoint reference.

## Contributing

Create a branch + open PR. All changes tested before merge.

## License

MIT
