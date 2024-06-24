yagami = [
      {
        "command": "task",
        "alias": "t",
        "description": "Manage tasks in Notion",
        "subcommands": [
          {
            "subcommand": "create",
            "alias": "c",
            "description": "Create a new task",
            "attributes": [
              {"name": "title", "alias":"t", "type": str, "required": True, "description": "Title of the task"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the task"},
              {"name": "categories", "alias":"c", "type": str, "required": False, "description": "List of categories associated with the task"},
              {"name": "notes",  "alias":"n", "type": str, "required": False, "description": "List of note IDs to link to the task"},
              {"name": "status",  "alias":"s", "type": str, "required": False, "description": "Status to the task"}
            ]
          },
          {
            "subcommand": "read",
            "alias": "r",
            "description": "Read a task",
            "attributes": [
              {"name": "title", "alias":"t", "type": str, "required": True, "description": "Title of the task to read"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the task to read"},
              {"name": "category", "alias":"c", "type": str, "required": False, "description": "Category associated with the task to read"},
              {"name": "notes",  "alias":"n", "type": str, "required": False, "description": "Note ID to link to the task to read"},
              {"name": "task_id", "alias":"ti", "type": str, "required": False, "description": "ID of the task to read"}
            ]
          },
          {
            "subcommand": "update",
            "alias": "u",
            "description": "Update an existing task",
            "attributes": [
              {"name": "task_id", "alias":"ti", "type": str, "required": False, "description": "ID of the task to update"},
              {"name": "title", "alias":"t", "type": str, "required": False, "description": "New title of the task"}
            ]
          },
          {
            "subcommand": "delete",
            "alias": "d",
            "description": "Delete a task",
            "attributes": [
              {"name": "task_id","alias":"ti", "type": str, "required": False, "description": "ID of the task to delete"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the task to delete"},
              {"name": "categories", "alias":"c","type": str, "required": False, "description": "List of categories of the task to delete"}
            ]
          }
        ]
      },
      {
        "command": "note",
        "alias": "n",
        "description": "Manage notes in Notion",
        "subcommands": [
          {
            "subcommand": "create",
            "alias": "c",
            "description": "Create a new note",
            "attributes": [
              {"name": "title", "alias":"t","type": str, "required": True, "description": "Title of the note"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the note"},
              {"name": "categories", "alias":"c","type": str, "required": False, "description": "List of Categories associated with the note"},
              {"name": "linked_notes","alias":"ln", "type": str, "required": False, "description": "List of note IDs this note links to"},
              {"name": "linked_tasks", "alias":"lt","type": str, "required": False, "description": "List of task IDs this note links to"}
            ]
          },
          {
            "subcommand": "read",
            "alias": "r",
            "description": "Read a note",
            "attributes": [
              {"name": "title", "alias":"t", "type": str, "required": True, "description": "Title of the note to read"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the note to read"},
              {"name": "category", "alias":"c", "type": str, "required": False, "description": "Category associated with the note to read"},
              {"name": "note_id", "alias":"ti", "type": str, "required": False, "description": "ID of the note to read"}
            ]
          },
          {
            "subcommand": "update",
            "alias": "u",
            "description": "Update an existing note",
            "attributes": [
              {"name": "note_id", "alias":"ni","type": str, "required": True, "description": "ID of the note to update"},
              {"name": "categories", "alias":"c","type": str, "required": False, "description": "Updated list of Categories associated with the note"},
            ]
          },
          {
            "subcommand": "delete",
            "alias": "d",
            "description": "Delete a note",
            "attributes": [
              {"name": "note_id", "alias":"ni", "type": str, "required": True, "description": "ID of the note to delete"},
              {"name": "list", "alias":"l", "type": str, "required": False, "description": "List associated with the note to delete"},
              {"name": "categories", "alias":"c", "type": str, "required": False, "description": "List of categories of the note to delete"}
            ]
          }
        ]
      }
    ]