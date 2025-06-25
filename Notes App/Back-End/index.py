from fastapi import FastAPI
from routes.note import note
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="../Front-End/static"), name="static")

app.include_router(note)