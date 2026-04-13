from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import Annotated, Union


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/todos", response_class=HTMLResponse)
async def show_todo_list(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse(
            request=request, 
            name="todos.html", 
            context={"todos": todos}
        )
    
    return JSONResponse(content=jsonable_encoder(todos))



@app.post("/todos", response_class=HTMLResponse)#zum erstellen der aufgaben (todos)
async def create_todo(request: Request, todo: Annotated[str, Form()]):
    
    todos.append(TODO(todo))
    
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"todos": todos}
    )



@app.put("/todos/{todo_id}", response_class=HTMLResponse) 
#zum verändern / bearbeiteb der aufgaben (todos) damit  es dynamisch bleibt
#ohne put und nur post wird nur das was als erstes gespeichert wurde aus der liste geladen 
async def update_todo_thingy(request: Request, todo_id: str, text: Annotated[str, Form()]):
    
    for index, EIN_todo in enumerate(todos):
        
        if str(EIN_todo.randomID_object_SAVE_HERE) == todo_id:
            EIN_todo.user_object_SAVE_HERE = text
            break
        
        
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"todos": todos}
    )     



@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def todo_done_not_done(request: Request, todo_id: str):
    
    for index, EIN_todo in enumerate(todos):
        
        if str(EIN_todo.randomID_object_SAVE_HERE) == todo_id:
            todos[index].done_oject_SAVE_HERE = not todos[index].done_oject_SAVE_HERE
            break
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"todos": todos}
    )



@app.post("/todos/{todo_id}/delete", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
    for index, EIN_todo in enumerate(todos):
        if str(EIN_todo.randomID_object_SAVE_HERE) == todo_id:
            del todos[index]
            break
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"todos": todos}
    )



class TODO:  #bauplant wie  die todo aussehen soll was sie enthalten soll auch technisch
    def __init__(self, text_from_user_input_field:str):
        self.randomID_object_SAVE_HERE = uuid4()
        self.user_object_SAVE_HERE = text_from_user_input_field
        self.done_oject_SAVE_HERE = True


#liste im RAM enthält nach bauplan erstellte todo
todos =  []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#nnotes
#html output section fixen css nötig / porftolio site zur hilfe
#date nnamen korrekt ändern
#nach usernamen fragen wird mit im post oben angezeigt
#speicherung vorerst in dict / liste
#häckchenbox entfernen
    