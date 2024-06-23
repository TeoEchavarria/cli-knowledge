# cli-knowledge

## Crear entorno virtual

```
python3 -m venv .venv
source .venv/bin/activate
```

## Intalacion de los paquetes

```
pip install -r requirements.txt 
```

## Crear un Token para integrarlo con Notion

Hazlo en https://www.notion.so/my-integrations añade el token directamente desde env como una variable, o ponlo como una variable de entorno de la forma:

```
export NOTION_TOKEN=[SECRET_KEY]
export TASK_DATABASE_ID=[TASK_ID]
export NOTE_DATABASE_ID=[NOTE_ID]
```

Para los ID, las primeras bases de datos tienen que crearse a mano. Aqui pueden ver como sacar el id de la base de datos : https://stackoverflow.com/questions/67728038/where-to-find-database-id-for-my-database-in-notion 

> En los 3 puntos de la database darle click a `View Database`, luego darle a los 3 puntos de la parte superior derecha, darle en `Connect to` y añadir la integracion que antes se creo