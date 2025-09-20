import io
import os
import glob
import base64
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageDraw
from ultralytics import YOLO

# --- Model loading ---
project_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(project_dir, os.pardir))

# Try to find a model file named like best*.pt in the root directory
candidate_models = sorted(glob.glob(os.path.join(root_dir, "best*.pt")))
if candidate_models:
    model_path = candidate_models[0]
else:
    fallback = os.path.join(root_dir, "best.pt")
    model_path = fallback if os.path.exists(fallback) else None

if not model_path or not os.path.exists(model_path):
    raise FileNotFoundError(
        f"Model file not found. Place trained weights (e.g., 'best.pt') in project root: {root_dir}"
    )

model = YOLO(model_path)

# --- FastAPI app ---
app = FastAPI(title="Ocean Plastics Waste Detection API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Detection(BaseModel):
    class_name: str
    confidence: float
    box: List[float]  # [x1, y1, x2, y2]

class PredictResponse(BaseModel):
    plastic_detections: List[Detection]
    plastic_count: int
    annotated_image_b64: str

@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile = File(...)):
    # Read file into PIL Image
    content = await file.read()
    image = Image.open(io.BytesIO(content)).convert("RGB")

    # Run inference
    results = model.predict(source=image, conf=0.5, verbose=False)

    # Prepare drawing
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    detections: List[Detection] = []
    plastic_count = 0

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[cls]

            # Only keep PLASTIC detections
            if class_name != "Plastic":
                continue

            plastic_count += 1

            x1, y1, x2, y2 = [float(v) for v in box.xyxy[0]]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1 - 10), f"{class_name} {confidence:.2f}", fill="red")

            detections.append(Detection(class_name=class_name, confidence=confidence, box=[x1, y1, x2, y2]))

    # Convert annotated image to base64
    buf = io.BytesIO()
    draw_image.save(buf, format="JPEG")
    annotated_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return PredictResponse(
        plastic_detections=detections,
        plastic_count=plastic_count,
        annotated_image_b64=annotated_b64,
    )

# To run locally:
# uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
