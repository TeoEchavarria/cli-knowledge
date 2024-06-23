class Note:
    def __init__(self, title, categories=None, linked_notes=None, linked_tasks=None, content=None):
        self.title = title
        self.categories = categories.split(',') if categories else []
        self.linked_notes = linked_notes.split(',') if linked_notes else []
        self.linked_tasks = linked_tasks.split(',') if linked_tasks else []
        self.content = content

    def to_dict(self):
        """Convertir la instancia a diccionario para API."""
        return {
            'title': self.title,
            'categories': self.categories,
            'linked_notes': self.linked_notes,
            'linked_tasks': self.linked_tasks,
            'content': self.content
        }