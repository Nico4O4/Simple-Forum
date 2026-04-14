from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated, Union


app = FastAPI()

jja2_templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def show_index_frontend(request: Request):
    return jja2_templates.TemplateResponse("index.html", {"request": request})


@app.get("/forum", response_class=HTMLResponse)
async def show_forum_beitraege(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        
        return jja2_templates.TemplateResponse(
            request=request, 
            name="response_from_server.html", 
            context={"beiträge_kiste": beitrag_speicher_list}
        )
    
    return JSONResponse(content=jsonable_encoder(beitrag_speicher_list))




@app.post("/forum", response_class=HTMLResponse)#zum erstellen der beiträge
async def create_beitrag(request: Request, post_platzhalter: Annotated[str, Form()]):
    
    beitrag_speicher_list.append(BLUEPRINT_BEITRAG(post_platzhalter))
    
    return jja2_templates.TemplateResponse(
        request=request,
        name="response_from_server.html",
        context={"beiträge_kiste": beitrag_speicher_list}
    )
#422 error kommt von hier vermutlich wegen post platzhaler etwas?
#post_platzhalter hat etwas mit dem htmx user input oder sowas zutun


@app.put("/forum/{forum_id}", response_class=HTMLResponse) 
#zum verändern / bearbeiteb der aufgaben (todos) damit  es dynamisch bleibt
#ohne put und nur post wird nur das was als erstes gespeichert wurde aus der liste geladen 
async def update_todo_thingy(request: Request, forum_id: str, text: Annotated[str, Form()]):
    
    for index, EIN_beitrag in enumerate(beitrag_speicher_list):
        
        if str(EIN_beitrag.randomID_object_SAVE_HERE) == forum_id:
            EIN_beitrag.user_object_SAVE_HERE = text
            break
        
        
    return jja2_templates.TemplateResponse(
        request=request,
        name="response_from_server.html",
        context={"beiträge_kiste": beitrag_speicher_list}
    )
#beiträge_kiste wird benutzt weil man die kompplette liste aktualisiert zurückbekommt
#dabei dient "ein_beitrag" als platzhalter für jedes einzelne objekt in der liste (ein objekt ist ein beitrag)


#@app.post("/forum/{forum_id}/toggle", response_class=HTMLResponse)
#async def todo_done_not_done(request: Request, todo_id: str):
#    
#    for index, EIN_todo in enumerate(todos):
#        
#        if str(EIN_todo.randomID_object_SAVE_HERE) == todo_id:
#            todos[index].done_oject_SAVE_HERE = not todos[index].done_oject_SAVE_HERE
#            break
#    return templates.TemplateResponse(
#        request=request,
#        name="todos.html",
#        context={"todos": todos}
#    )
#zukünnftiger like button POST request
#einfacch mit button dann POST request und +1 erhöhren sobald die route ausgeführt wurde
#davor variable mit 0 likes definieren als startwert (global)


@app.post("/forum/{forum_id}/delete", response_class=HTMLResponse)
async def delete_beitrag(request: Request, todo_id: str):
    for index, EIN_beitrag in enumerate(beitrag_speicher_list):
        if str(EIN_beitrag.randomID_object_SAVE_HERE) == todo_id:
            del beitrag_speicher_list[index]
            break
    return jja2_templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"beiträge_kiste": beitrag_speicher_list}
    )



class BLUEPRINT_BEITRAG:  #bauplan wie  der beitrag aussehen soll und was er enthalten soll
    def __init__(self, text_username, text_from_user_input_field :str):
        self.randomID_object_SAVE_HERE = uuid4()
        self.username_save = text_username
        self.user_object_SAVE_HERE = text_from_user_input_field
        self.done_oject_SAVE_HERE = True



#liste im RAM enthält nach bauplan erstellte todo
beitrag_speicher_list =  []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#nnotes
#html output section fixen css nötig / porftolio site zur hilfe
#date nnamen korrekt ändern
#nach usernamen fragen wird mit im post oben angezeigt
#speicherung vorerst in dict / liste
#häckchenbox entfernen
    