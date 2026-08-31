from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from utils import calculate_phash, are_images_near_duplicates

app = FastAPI()

# Enable CORS so your React frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    processed_files = []
    
    # 1. Save and compute hashes for all uploaded files
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_hash = calculate_phash(file_path)
        if file_hash:
            processed_files.append({
                "filename": file.filename,
                "path": file_path,
                "hash": file_hash
            })

    # 2. Group duplicates together
    duplicate_groups = []
    visited = set()

    for i in range(len(processed_files)):
        if i in visited:
            continue
        
        current_group = [processed_files[i]["filename"]]
        visited.add(i)
        
        for j in range(i + 1, len(processed_files)):
            if j not in visited:
                if are_images_near_duplicates(processed_files[i]["hash"], processed_files[j]["hash"]):
                    current_group.append(processed_files[j]["filename"])
                    visited.add(j)
                    
        # Only add groups that actually contain duplicates
        if len(current_group) > 1:
            duplicate_groups.append(current_group)

    return {"duplicate_groups": duplicate_groups}