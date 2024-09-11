
from fastapi import FastAPI, status, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import markdown
from fastapi.responses import  HTMLResponse
import language_tool_python

from utils import save_file, read_note, get_all_notes

app = FastAPI(
    title="Markdown Note Taking App",
    description="Markdown Note Taking App",
    version="1.0.0",

)

class Note(BaseModel):
    note: str

@app.post("/check-grammar")
def check_grammar(note: Note):
    tool = language_tool_python.LanguageTool("en-US")
    matches = tool.check(note.note)
    return_value = {}
    for match in matches:
        return_value[match.offset] = {
            "message": match.message,
            "replacements": match.replacements
        }
    return return_value
    
    
    
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    data = await file.read()
    saved = save_file(file.filename, data)
    print(saved)
    if saved:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "detail": "File saved!"
            }
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Error in saving the file"
        }
    )
@app.get("/")
def get_notes():
    notes = get_all_notes()

    if not notes:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="No notes found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "notes": notes
        }
    )

@app.get("/{note_name}")
def get_note(note_name: str):
    note = read_note(note_name)
    if not note:
        return JSONResponse(

            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "Note not found"
            }
        )
    html_context = markdown.markdown(note)
    return HTMLResponse(content=html_context)