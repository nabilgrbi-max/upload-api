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
        # 1. On sépare l'en-tête (ex: "data:audio/wav;base64,") des données
        header, encoded_data = payload.data_uri.split(",", 1)
        
        # 2. On décode le texte Base64 pour obtenir les données audio pures
        audio_data = base64.b64decode(encoded_data)

        # On envoie maintenant les données pures à Cloudinary
        upload_result = cloudinary.uploader.upload(
            audio_data, # On utilise les données décodées et non plus le texte complet
            resource_type = "video", # Cloudinary gère l'audio dans la catégorie "video"
            upload_preset = payload.upload_preset,
            folder = "spots_radio_tts" # Optionnel : pour ranger les fichiers
        )
        
        # On renvoie la réponse de Cloudinary (qui contient la secure_url)
        return upload_result

    except Exception as e:
        # En cas d'erreur, on renvoie un message clair
        raise HTTPException(status_code=500, detail=str(e))
