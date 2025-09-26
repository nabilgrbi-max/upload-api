import os
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader

# Configuration de Cloudinary avec les clés secrètes de Render
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Modèle pour s'assurer que Bubble nous envoie les bonnes données
class UploadPayload(BaseModel):
    data_uri: str
    upload_preset: str

app = FastAPI()

@app.get("/")
def racine():
    return {"message": "API Adeasy.io prête pour l'upload !"}

# Notre nouvelle route qui fait le travail
@app.post("/upload_from_data_uri/")
def upload_from_data_uri(payload: UploadPayload):
    try:
        # On envoie la Data URI directement à Cloudinary, qui sait la décoder
        upload_result = cloudinary.uploader.upload(
            payload.data_uri,
            resource_type = "video", # Cloudinary gère l'audio dans la catégorie "video"
            upload_preset = payload.upload_preset,
            folder = "spots_radio_tts" # Optionnel : pour ranger les fichiers
        )
        
        # On renvoie la réponse de Cloudinary (qui contient la secure_url)
        return upload_result

    except Exception as e:
        # En cas d'erreur, on renvoie un message clair
        raise HTTPException(status_code=500, detail=str(e))