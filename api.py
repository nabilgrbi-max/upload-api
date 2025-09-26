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
        # On "déballe" la Data URI reçue de Bubble
        header, encoded_data = payload.data_uri.split(",", 1)
        audio_data = base64.b64decode(encoded_data)

        # On envoie les données pures à Cloudinary
        upload_result = cloudinary.uploader.upload(
            audio_data,
            resource_type = "video",
            upload_preset = payload.upload_preset,
            folder = "spots_radio_tts"
        )
        
        return upload_result

    except Exception as e:
        # NOUVEAU : On affiche l'erreur détaillée dans les logs de Render
        print(f"ERREUR DÉTAILLÉE : {e}")
        
        # On renvoie toujours une erreur à Bubble
        raise HTTPException(status_code=500, detail=str(e))
