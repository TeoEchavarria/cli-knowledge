class Task:
    def __init__(self, title, categories=None, notes=None, content=None):
        self.title = title
        self.categories = categories.split(',') if categories else []
        self.notes = notes.split(',') if notes else []
        self.content = content

    def to_dict(self):
        """Convertir la instancia a diccionario para API."""
        return {
            'title': self.title,
            'categories': self.categories,
            'notes': self.notes,
            'content': self.content
        }