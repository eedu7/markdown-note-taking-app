import os
from fastapi import HTTPException,status

BASE_PATH = "markdowns/"

def save_file(file_name: str, data: str):
    exist = os.path.exists(BASE_PATH + file_name)
    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File {file_name} already exists"
        )

    try:
        with open(BASE_PATH + file_name, 'wb') as f:
            f.write(data)
            f.close()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def read_note(file_name):
    if not file_name.endswith(".md"):
        file_name = file_name + ".md"
    try:
        with open(BASE_PATH + file_name, 'r') as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_notes():
    notes = [note for note in os.listdir(BASE_PATH)]
    return notes