from fastapi import FastAPI, Path
from typing import Optional # To remove required field
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    name: str
    description: str
    status: str

class UpdateTask(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Filler Tasks
# Main list of todo, all tasks are put here
tasklist = {
    1: Task(
        name = "Walk the dog",
        description = "Don't forget to walk the dog at 10 A.M.",
        status = "Incompleted"
    ),

    2: Task(
        name = "Laundry",
        description = "Wash uniforms before school on Monday",
        status = "Incompleted"
    ),

    3: Task(
        name = "Dishes",
        description = "Don't forget to put them in the dryer",
        status = "Completed"
    )
}

# List for filtered tasks
# Filtered based on status
# Used for FILTER BY STATUS method
filteredlist = {
    1: Task(
        name = "Filtered",
        description = "Filtered",
        status = "Filtered"
    ),
}

# GET METHOD
@app.get("/")
def index():
    return {"Hello": "This is a To-Do List made by FastAPI"}

# GET TASK BY ID
# GET METHOD
@app.get("/get-task/{task_id}")
def get_task(task_id: int = Path(description="ID of Task")):
    return tasklist[task_id]

# GET TASK BY NAME
# GET METHOD
@app.get("/get-task-by-name/{name}")
def get_task(name: str):
    for task_id in tasklist:
        if tasklist[task_id].name == name:
            return tasklist[task_id]
    return {"Error":"Task does not exist"}

# FILTER BY STATUS
# GET METHOD
# Example: List all tasks that are completed.
@app.get("/filter-by-status/{status}")
def get_task(status: str):
    global filteredlist # Global to avoid UnboundLocalError 
    filteredlist.clear() # Clear list (clear filter)

    # Traverses through all tasks
    for task_id in tasklist:

        # If current task's status is the status that is requested
        # Current task is appended to the filteredlist
        if tasklist[task_id].status == status:
            filteredlist[task_id] = tasklist[task_id]

    # Return filteredlist after all tasks are checked
    return filteredlist

# ADD NEW TASK
# POST METHOD
@app.post("/add-task/")
def add_task(task_id: int, task : Task):
    if task_id in tasklist:
        return {"Error" : "Task already exists"}
    tasklist[task_id] = task
    return tasklist[task_id]

# UPDATE TASK (NAME, DESC, STATUS)
# PUT METHOD
@app.put("/update-task/{task_id}")
def update_task(task_id: int, task: UpdateTask):
    if task_id not in tasklist:
        return {"Error":"Task does not exist"}

    if task.name != None:
        tasklist[task_id].name = task.name

    if task.description != None:
        tasklist[task_id].description = task.description

    if task.status != None:
        tasklist[task_id].status = task.status
    
    return tasklist[task_id]

# DELETE METHOD
@app.delete("/delete-task/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasklist:
        return {"Error":"The task does not exist."}

    del tasklist[task_id]
    return{"Task":"Deleted successfully."}