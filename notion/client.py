from notion_client import Client
from config.env import token_notion, task_id_database, note_id_database
import requests

def notionMain():
    print(token_notion)
    notion = Client(auth=token_notion)
    database_id = task_id_database
    response = notion.databases.query(
    **{
        "database_id": database_id
    })
    print(response)