import os
import base64
import uuid
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

# La route qui fait le travail, version finale et robuste
@app.post("/upload_from_data_uri/")
def upload_from_data_uri(payload: UploadPayload):
    # On crée un nom de fichier temporaire unique dans un dossier accessible
    temp_filename = f"/tmp/{uuid.uuid4()}.mp3"
    
    try:
        # 1. On décode la Data URI pour obtenir les données audio pures
        header, encoded_data = payload.data_uri.split(",", 1)
        audio_data = base64.b64decode(encoded_data)

        # 2. On écrit ces données dans un vrai fichier sur le serveur
        with open(temp_filename, "wb") as f:
            f.write(audio_data)

        # 3. On envoie ce fichier temporaire à Cloudinary
        upload_result = cloudinary.uploader.upload(
            temp_filename,
            resource_type = "video",
            upload_preset = payload.upload_preset,
            folder = "spots_radio_tts"
        )
        
        return upload_result

    except Exception as e:
        print(f"ERREUR DÉTAILLÉE : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 4. Quoi qu'il arrive, on supprime le fichier temporaire pour nettoyer
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
