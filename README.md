# Ocean Plastic Waste Detection

Detect and visualize plastic waste in images using a FastAPI backend (Ultralytics YOLO) and a modern React (Vite) frontend.

This project is built for clean showcasing on resumes/portfolios: simple setup, clear UI, and a single, polished release.

## Highlights

- Plastic-only detection using YOLO with configurable confidence threshold (default: `0.5`).
- React (Vite) UI for quick uploads, with plastic count prominently displayed.
- Annotated image preview (server-side rendering) returned as Base64.
- Clean API surface: `/health` and `/predict`.

## Live Demo (optional)

- Frontend: <your-demo-url>
- Backend: self-hosted or cloud (Render/Railway/Azure/GCP/AWS)

> Tip: Deploy the frontend (Netlify/Vercel) and point it to your backend via `VITE_API_BASE`.

## Tech Stack

- Backend: `FastAPI`, `Uvicorn`, `Ultralytics YOLO`, `OpenCV`, `Pillow`
- Frontend: `React 18`, `Vite`
- Language: Python 3.10+, Node.js 18+

## Repository Structure

- `backend/main.py` — FastAPI app that loads YOLO weights; exposes `/health` and `/predict` (plastic-only).
- `frontend/` — React (Vite) app to upload an image and view detections (count + annotated preview).
- `best.pt` — Your trained YOLO weights at project root (auto-discovered by backend).

## Getting Started (Windows PowerShell)

Run commands from the project root: `d:\Ocean\Ocean-Plastic-Waste-Detection`.

### 1) Backend (FastAPI)

1. Create and activate a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   python -m pip install -r requirements.txt
   ```

3. Model weights:

   - Ensure `best.pt` (or any `best*.pt`) exists at the repo root.
   - Example: `d:\Ocean\Ocean-Plastic-Waste-Detection\best.pt`

4. Start the API server:

   ```powershell
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. Health check:

   - Open http://127.0.0.1:8000/health — expected: `{ "status": "ok" }`

### 2) Frontend (React + Vite)

From `frontend/`:

```powershell
npm install
npm run dev
```

Open the URL printed by Vite, e.g. http://127.0.0.1:5173

Configure API base URL (optional) — create `frontend/.env`:

```env
VITE_API_BASE=http://127.0.0.1:8000
```

Restart `npm run dev` after changing `.env`.

## Usage

1. Start the backend and frontend.
2. In the UI, upload an image with ocean/beach scenes.
3. The app returns:
   - A plastic count (chips hidden; shows count only).
   - An annotated preview (downloadable or view-only depending on UI settings).

## API Reference

- `GET /health`
  - Returns `{ "status": "ok" }`.

- `POST /predict`
  - Content-Type: `multipart/form-data`
  - Field: `file` (image)
  - Response JSON:
    - `plastic_detections`: `[ { class_name: "Plastic", confidence, box: [x1,y1,x2,y2] }, ... ]`
    - `plastic_count`: number
    - `annotated_image_b64`: Base64 JPEG of annotated result

## Configuration & Troubleshooting

- Confidence threshold: Default is `0.5` in `backend/main.py`. Increase to reduce false positives.
- Model not found: Place `best.pt` in the project root, or support an env var like `MODEL_PATH`.
- Port already in use: Change `--port` when starting uvicorn (e.g., `--port 8001`) and set `VITE_API_BASE` accordingly.
- CORS: Enabled for local dev in `backend/main.py`. If hosts/ports change, point the frontend to the correct API.
- Large dependency wheels: Upgrading `pip` first usually helps with OpenCV/Ultralytics installs.

## Production / Deployment

- Frontend build:

  ```powershell
  npm run build
  ```

  Outputs static files to `frontend/dist/`.

- Hosting options:
  - Frontend: Netlify / Vercel / GitHub Pages (serve `dist/`).
  - Backend: Render / Railway / Azure App Service / GCP Cloud Run / AWS.

- Environment:
  - Set `VITE_API_BASE` to the deployed backend URL for the frontend.

## Screenshots (optional)

Add images under `assets/` and reference them here for your portfolio/resume.

## License

Add your license of choice (e.g., MIT) or keep private.

## Acknowledgements

- Ultralytics YOLO for detection models.
- React + Vite for a fast developer experience.