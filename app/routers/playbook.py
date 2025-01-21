import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import subprocess

router = APIRouter()

PLAYBOOKS_DIR = "../playbooks"  # 替换为实际的路径

@router.post("/")
async def run_playbook(file: UploadFile = File(...)):
    try:
        # 确保 playbooks 目录存在
        os.makedirs(PLAYBOOKS_DIR, exist_ok=True)

        # 保存上传的文件
        file_path = os.path.join(PLAYBOOKS_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 使用 ansible-playbook 命令执行 playbook
        result = subprocess.run(["ansible-playbook", file_path], capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Ansible playbook 执行失败: {result.stderr}")

        return {"message": "Playbook 执行成功", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 