
from pathlib import Path
import shutil
import tempfile
from pydantic import BaseModel
from app.transcription_metrics import calculate_transcription_metrics
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.gnani_client import GnaniSTTClient

app = FastAPI(
    title="BENCHIN",
    description="Gnani-powered speech transcription",
    version="1.0.0",
)

class EvaluationRequest(BaseModel):
    reference: str
    hypothesis: str

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".aac", ".m4a"}

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    extension = Path(audio_file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format.",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            shutil.copyfileobj(audio_file.file, temp_file)
            temp_path = Path(temp_file.name)

        client = GnaniSTTClient()

        result = client.transcribe(
            audio_path=str(temp_path),
            language_code="gu-IN,en-IN",
            output_format="codemix",
        )

        return {
            "success": True,
            "transcript": result.get("transcript", ""),
            "model": result.get("model"),
            "detected_language_code": result.get(
                "detected_language_code"
            ),
            "processing_time": result.get("processing_time"),
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Transcription failed. Check the server logs.",
        ) from error

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

        await audio_file.close()

@app.post("/evaluate")
async def evaluate_transcription(request: EvaluationRequest):
    result = calculate_transcription_metrics(
        reference=request.reference,
        hypothesis=request.hypothesis,
    )

    return {
        "reference_words": result.reference_words,
        "substitutions": result.substitutions,
        "deletions": result.deletions,
        "insertions": result.insertions,
        "wer": result.wer,
        "cer": result.cer,
    }
