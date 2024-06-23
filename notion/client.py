from notion_client import Client
from config.env import token_notion, task_id_database, note_id_database

notion = Client(auth=token_notion)

def create(type, properties, childrens):
    database_id = task_id_database if type == "task" else note_id_database
    notion.pages.create(parent={"database_id": database_id}, properties=properties, children=childrens)