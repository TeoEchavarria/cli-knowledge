from notion.client import create
from utils.cli import open_file

def run(args):
    content = open_file()
    new_note_properties = {
    "Title": {
        "title": [
            {
                "text": {
                    "content": args["title"]
                }
            }
        ]
    },
    "List": {
        "select": {
            "name" :  args["list"]
         } if args["list"] != None else None
    },
    "Categories": {
        "multi_select": [
            {"name" : category} for category in args["categories"].split(",")
        ] if args["categories"] != None else []
    },
    # "Notes": {
    #     "relation": [
    #         {
    #             "name" : note_id for note_id in args["notes"].split(",") 
    #         } if args["notes"] != None else {}
    #     ]
    # }
    # Añade más propiedades según la estructura de tu base de datos
}
    # Añade la tarea a la base de datos
    new_note = create("note", new_note_properties, content)
