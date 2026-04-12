from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated, Union
import json

#get - anzeigen
#post - erstellen
#put - aktualisieren
#delete - löschen
#patch - teilweise aktualisieren (nur bestimmte Felder)

app = FastAPI()

jja2_templates = Jinja2Templates(directory=r"C:\Users\nicop\Desktop\Simple Forum\style_stuff")

@app.get("/", response_class=HTMLResponse)
async def main_endpoint_start(request: Request):

    return jja2_templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )
    


@app.post("/beitrag_posten", response_class=HTMLResponse)
async def erstelle_beitrag(
        request: Request,
        username: str = Form("lolololo"),
        nachricht: str = Form()
    ):

    
    return jja2_templates.TemplateResponse(
        "update_stuff.html",
        {"request": request, 
         "username": username,
         "nachricht": nachricht}
    )
    





#Notes
#one html file only? with the htmx and jinja2 stuff
#
#
#
#
#
#