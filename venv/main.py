from fastapi import FastAPI, Path
from typing import Optional # To remove required field
from pydantic import BaseModel

app = FastAPI()

## ----------------------------------------------------------- ##
## ----------------------------------------------------------- ##
## ----------------------- BASE MODELS ----------------------- ##
## ----------------------------------------------------------- ##
## ----------------------------------------------------------- ##

class User(BaseModel):
    username: str
    email: str
    auth: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    auth: Optional[str] = None

class Task(BaseModel):
    name: str
    description: str
    status: str
    username: str

class UpdateTask(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    username: Optional[str] = None

## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##
## ---------------------- DICTIONARIES ---------------------- ##
## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##

# Main list of todo, all tasks are put here
tasklist = {
    1: Task(
        name = "Walk the dog",
        description = "Don't forget to walk the dog at 10 A.M.",
        status = "Incompleted",
        username = "kimberlymazel"
    ),

    2: Task(
        name = "Laundry",
        description = "Wash uniforms before school on Monday",
        status = "Incompleted",
        username = "kimberlymazel"
    ),

    3: Task(
        name = "Dishes",
        description = "Don't forget to put them in the dryer",
        status = "Completed",
        username = "bagzmate"
    )
}

# Main list of users, all users are put here
userlist = {
    1: User(
        username = "kimberlymazel",
        email = "km@gmail.com",
        auth = "google"
    ),

    2: User(
        username = "bagzmate",
        email = "bagzmate@binus.ac.id",
        auth = "github"
    )
}

# List for filtered tasks
filteredlist = {
    1: Task(
        name = "Filtered",
        description = "Filtered",
        status = "Filtered",
        username = "Filtered"
    ),
}

# List for filtered users
filteredusers = {
    1: User(
        username = "filtered",
        email = "filtered",
        auth = "filtered"
    )
}

# INDEX
@app.get("/")
def index():
    return {"Hello": "This is a To-Do List made by FastAPI"}

## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##
## ---------------------- USER METHODS ---------------------- ##
## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##

# GET ALL USERS
@app.get("/get-userlist/")
def get_all_users():
    return userlist

# GET USER BY ID
@app.get("/get-user/{user_id}")
def get_user(user_id: int = Path(description="ID of User")):
    return userlist[user_id]

# GET USER BY USERNAME
@app.get("/get-user-by-username/{username}")
def get_user(username: str):
    for user_id in userlist:
        if userlist[user_id].username == username:
            return userlist[user_id]
    return {"Error":"User does not exist"}

# FILTER USER BY AUTHENTICATION
# Example: List all users from google
@app.get("/filter-by-auth/{auth}")
def get_user(auth: str):
    global filteredusers # Global to avoid UnboundLocalError 
    filteredusers.clear() # Clear list (clear filter)

    # Traverses through all users
    for user_id in userlist:

        # If current user's auth is the auth that is requested
        # Current user is appended to filteredusers
        if userlist[user_id].auth == auth:
            filteredusers[user_id] = userlist[user_id]

    # Return filteredusers after all tasks are checked
    return filteredusers

# ADD NEW USER
@app.post("/add-user/")
def add_user(user_id: int, user : User):
    if user_id in userlist:
        return {"Error" : "User already exists"}
    userlist[user_id] = user
    return userlist[user_id]

# UPDATE USER (USERNAME, EMAIL, AUTH)
@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in userlist:
        return {"Error":"User does not exist"}

    if user.username != None:
        userlist[user_id].username = user.username

    if user.email != None:
        userlist[user_id].email = user.email

    if user.auth != None:
        userlist[user_id].auth = user.auth
    
    return userlist[user_id]

# DELETE USER
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    if user_id not in userlist:
        return {"Error":"The user does not exist."}

    del userlist[user_id]
    return{"User":"Deleted successfully."}

## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##
## ---------------------- TASK METHODS ---------------------- ##
## ---------------------------------------------------------- ##
## ---------------------------------------------------------- ##

# GET ALL TASKS
@app.get("/get-tasklist/")
def get_all_task():
    return tasklist

# GET TASK BY ID
@app.get("/get-task/{task_id}")
def get_task(task_id: int = Path(description="ID of Task")):
    return tasklist[task_id]

# GET TASK BY NAME
@app.get("/get-task-by-name/{name}")
def get_task(name: str):
    for task_id in tasklist:
        if tasklist[task_id].name == name:
            return tasklist[task_id]
    return {"Error":"Task does not exist"}

# FILTER BY STATUS
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

# FILTER BY USERNAME
# Example: List all tasks that are by user1.
@app.get("/filter-by-user/{username}")
def get_task(username: str):
    global filteredlist # Global to avoid UnboundLocalError 
    filteredlist.clear() # Clear list (clear filter)

    # Traverses through all tasks
    for task_id in tasklist:

        # If current task's username is the username that is requested
        # Current task is appended to the filteredlist
        if tasklist[task_id].username == username:
            filteredlist[task_id] = tasklist[task_id]

    # Return filteredlist after all tasks are checked
    return filteredlist

# ADD NEW TASK
@app.post("/add-task/")
def add_task(task_id: int, task : Task):
    if task_id in tasklist:
        return {"Error" : "Task already exists"}
    tasklist[task_id] = task
    return tasklist[task_id]

# UPDATE TASK (NAME, DESC, STATUS, USERNAME)
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

    if task.username != None:
        tasklist[task_id].username =  task.username
    
    return tasklist[task_id]

# DELETE TASK
@app.delete("/delete-task/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasklist:
        return {"Error":"The task does not exist."}

    del tasklist[task_id]
    return{"Task":"Deleted successfully."}