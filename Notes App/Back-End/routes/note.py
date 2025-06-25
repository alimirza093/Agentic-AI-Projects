from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schema.note import NoteEntity , NoteEntityList
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from datetime import datetime

note = APIRouter()

templates = Jinja2Templates(directory="../Front-End/templates")


@note.get("/", response_class=HTMLResponse)

# def read_item(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
@note.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    docs = conn.Notepad.Notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append(
            {
                "note": str(doc["note"]),
                "id": str(doc["_id"]),
                "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

    return templates.TemplateResponse(
        "index.html" , {"request": request , "docs": new_docs}
    )

@note.post("/")
async def add_item(request: Request):
    form = await request.form()
    if form["note"] == "":
        return RedirectResponse(url="/", status_code=303)
    new_note = dict(form)
    new_note["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = conn.Notepad.Notes.insert_one(new_note)
    return RedirectResponse(url="/", status_code=303)


@note.get("/notes")
def read_item_note(request: Request):
    return templates.TemplateResponse(
        "notes.html" , {"request": request}
    )

    