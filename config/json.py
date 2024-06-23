yagami = {
    "commands": [
      {
        "command": "task",
        "description": "Manage tasks in Notion",
        "subcommands": [
          {
            "subcommand": "create",
            "description": "Create a new task",
            "attributes": [
              {"name": "title", "type": "string", "required": True, "description": "Title of the task"},
              {"name": "categories", "type": "string", "required": False, "description": "List of categories associated with the task"},
              {"name": "notes", "type": "list", "required": False, "description": "List of note IDs to link to the task"}
            ]
          },
          {
            "subcommand": "update",
            "description": "Update an existing task",
            "attributes": [
              {"name": "task_id", "type": "string", "required": False, "description": "ID of the task to update"},
              {"name": "title", "type": "string", "required": False, "description": "New title of the task"}
            ]
          },
          {
            "subcommand": "delete",
            "description": "Delete a task",
            "attributes": [
              {"name": "task_id", "type": "string", "required": False, "description": "ID of the task to delete"},
              {"name": "categories", "type": "string", "required": False, "description": "List of categories of the task to delete"}
            ]
          }
        ]
      },
      {
        "command": "note",
        "description": "Manage notes in Notion",
        "subcommands": [
          {
            "subcommand": "create",
            "description": "Create a new note",
            "attributes": [
              {"name": "title", "type": "string", "required": True, "description": "Title of the note"},
              {"name": "categories", "type": "string", "required": False, "description": "List of Categories associated with the note"},
              {"name": "linked_notes", "type": "list", "required": False, "description": "List of note IDs this note links to"},
              {"name": "linked_tasks", "type": "list", "required": False, "description": "List of task IDs this note links to"}
            ]
          },
          {
            "subcommand": "update",
            "description": "Update an existing note",
            "attributes": [
              {"name": "note_id", "type": "string", "required": True, "description": "ID of the note to update"},
              {"name": "categories", "type": "string", "required": False, "description": "Updated list of Categories associated with the note"},
              {"name": "linked_notes", "type": "list", "required": False, "description": "Updated list of linked note IDs"},
              {"name": "linked_tasks", "type": "list", "required": False, "description": "Updated list of task IDs this note links to"}
            ]
          },
          {
            "subcommand": "delete",
            "description": "Delete a note",
            "attributes": [
              {"name": "note_id", "type": "string", "required": True, "description": "ID of the note to delete"},
              {"name": "categories", "type": "string", "required": False, "description": "List of categories of the note to delete"}
            ]
          }
        ]
      }
    ]
  }