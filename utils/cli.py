import tempfile
import os
import subprocess
from utils.notion import markdown_to_notion

def open_file():
    # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file_path = temp_file.name

    # Abre el archivo temporal con un editor de texto
    editor = os.getenv('EDITOR', 'vim')  # Usa el editor por defecto del sistema, o nano si no hay ninguno definido
    subprocess.run([editor, temp_file_path])

    # Lee el contenido del archivo después de cerrar el editor
    with open(temp_file_path, 'r') as file:
        contenido = file.read()
        
    # Elimina el archivo temporal
    os.unlink(temp_file_path)
    
    return markdown_to_notion(contenido)