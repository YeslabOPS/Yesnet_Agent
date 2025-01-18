import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import subprocess

router = APIRouter()

PLAYBOOKS_DIR = "../playbooks"  # Replace with your actual path

@router.post("/")
async def run_playbook(file: UploadFile = File(...)):
    try:
        # Ensure the playbooks directory exists
        os.makedirs(PLAYBOOKS_DIR, exist_ok=True)

        # Save the uploaded file
        file_path = os.path.join(PLAYBOOKS_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Execute the playbook using ansible-playbook command
        result = subprocess.run(["ansible-playbook", file_path], capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Ansible playbook execution failed: {result.stderr}")

        return {"message": "Playbook executed successfully", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 