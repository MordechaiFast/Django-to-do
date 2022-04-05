"""Takes existing json to-do list and put it in the Django db.
Only works by running in the Django shell"""

import json
from pathlib import Path

file_name = Path(input("Enter json To-do list path"))
with open(file_name) as file:
    db = json.load(file)

from todo_app.models import ToDoList, ToDoItem
new_list = ToDoList(title=file_name.stem)
new_list.save()

for item in db:
    new_item = ToDoItem(title=item['Description'], todo_list=new_list)
    new_item.save()