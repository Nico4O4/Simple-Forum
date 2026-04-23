from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated, Union
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

#für beiträge
beitrag_speicher_list =  []

jja2_templates = Jinja2Templates(directory="templates")

default_usr = "Anonym"


@app.get("/", response_class=HTMLResponse)
async def show_index_frontend(request: Request):

    return jja2_templates.TemplateResponse(
        request=request, 
        name="index.html"
        )



@app.post("/hochladen", response_class=HTMLResponse)
async def create_beitrag(request: Request, kommentar_von_usersky = Form(), 
                         username_usersky = Form(default_usr)
                         ):

    return jja2_templates.TemplateResponse(    
        request=request,
        name="response_from_server.html",
        context={"kommentar_user_KEY": kommentar_von_usersky, 
                    "username_KEY": username_usersky}
        )



@app.post("/ErneutPosten", response_class=HTMLResponse)
async def create_new_beitrag(request: Request, neuer_kommentar_user = Form(), neuer_username_user = Form(default_usr)):
    
    beitrag_speicher_list.append({
        "neuer_kommentar_user_KEY": neuer_kommentar_user, 
        "neuer_username_user_KEY": neuer_username_user
    })
        
    return RedirectResponse("/", status_code=303)
    #für updates oder sowas?

#KEY muss gleich heisen wie variable im TEMPLATE VON JINJA2 damit ein austausch stattfinden kann
#VALUE kann sonst wie heisen es enthält mein INPUT (DATEN) vom index.html (input feld)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#--notes--
#wenn man zur site gebracht wird per post request nochmals ne art endpoint logik / upload
#logik schreiben das man weiterhin posts schreiben kann