# AGENTS.md — 智教通 (AI Intelligent Teaching Platform)

## Project Context

Competition project: 湖南省第22届大学生计算机程序设计竞赛 (Web应用开发类).
**Deadline: 2026-07-21 24:00.**

Dual-end web application: **teacher side** (demand guidance, tool management, data dashboard) + **student side** (tool plaza, AI Q&A, learning records). See `C:\Users\Lenovo\Desktop\claude\3\项目梳理.md` for full requirements.

## Architecture

```
Frontend (Vue3 + Element Plus) → Backend (Python FastAPI) → MySQL
                                                    ↓
                                              DeepSeek API (text-only Q&A)
                                                    ↓
                                        师大智能体平台 (tool creation, external)
```

Two core capabilities:
1. **AI Q&A** — DeepSeek API for text-based learning interactions
2. **Tool Plaza** — curated tools (文/理 classified), links to 师大平台 for complex creation

Recommendation engine uses **if-else matching** (not AI). Preset tools stored in `tools` table with `is_preset=true`.

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Vue 3, Element Plus, Vite, Axios |
| Backend | Python FastAPI, SQLAlchemy, PyMySQL |
| Database | MySQL 8.0 |
| AI | DeepSeek API (model: dsv4) |
| Deploy | Nginx + uvicorn |

## Development Strategy

**Clone a GitHub template + AI-assisted改造.** Team is education-tech majors, not CS — leverage AI tools heavily.

Recommended templates: vue-pure-admin, vue-vben-admin, vue-admin-better.

## Key Constraints

- **Must have backend + database** — pure frontend/HTML won't qualify for competition
- **Must be deployable and runnable** — judges will access live
- **Code and docs must be original** — templates OK but require significant modification
- **All 7 design documents are required** — no shortcuts
- Every feature must **run and be verified before moving on** — no accumulating untested code
- AI (DeepSeek API) only handles **text Q&A** — cannot create tools or build workflows

## Teacher Side Flow

1. Login → Select subject area (文/理) → Select teaching need → System recommends tools (if-else)
2. "My Tools" → Create via template (modify prompt + params → save) OR jump to 师大平台
3. Share tools via link/QR code
4. Data dashboard: usage stats, trends, tool rankings

## Student Side Flow

1. Enter via shared link (no login) OR browse 工具广场 (文/理 classified)
2. Use AI Q&A or specific tools
3. View learning history

## Important Directories (once code exists)

- `source/frontend/` — Vue3 application
- `source/backend/` — FastAPI server
- See `项目记忆文件.md` at `C:\Users\Lenovo\Desktop\claude\3\` for progress tracking

## Verification

After any change, verify:
- Backend starts: `uvicorn main:app --reload`
- Frontend starts: `npm run dev`
- Database connection works
- DeepSeek API responds
- No console errors in browser

## Don't

- Don't implement tool creation inside the web app — that's 师大平台's job
- Don't use AI for recommendation logic — keep it simple with condition matching
- Don't write all code before testing — verify each piece incrementally
- Don't skip database design — establish tables early, avoid frequent schema changes
