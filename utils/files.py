
def initial_markdown_to_list_dict():
    from cli.actions.create_note import run
    from utils.notion import markdown_to_notion
    import os

    # Definir la ruta de la carpeta
    folder_path = 'knowledge/notes'

    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):  # Asegurarse de que el archivo es un Markdown
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                contenido_md = markdown_to_notion(file.read())
                # Aplicar la función al contenido
                run({ "title": filename.replace("md", ""), "list": None, "categories": None}, contenido_md)
                #resultado = run({}, contenido_md)
                print(f'Resultado para {filename}')

def list_dict_to_markdown(data_list, data_dict):
    markdown = []

    # Page details
    markdown.append(f"# Notion Page: {data_dict['properties']['Title']['title'][0]['plain_text']}")
    markdown.append("\n## Page Details")
    markdown.append(f"- **ID**: {data_dict['id']}")
    markdown.append(f"- **Created Time**: {data_dict['created_time']}")
    markdown.append(f"- **Last Edited Time**: {data_dict['last_edited_time']}")
    markdown.append(f"- **Created By**: {data_dict['created_by']['id']}")
    markdown.append(f"- **Last Edited By**: {data_dict['last_edited_by']['id']}")
    markdown.append(f"- **Parent Database ID**: {data_dict['parent']['database_id']}")
    markdown.append(f"- **Archived**: {data_dict['archived']}")
    markdown.append(f"- **In Trash**: {data_dict['in_trash']}")
    markdown.append(f"- **URL**: [Note]({data_dict['url']})")

    # Properties
    markdown.append("\n## Properties")
    markdown.append("- **Notes** (relation): Empty")
    categories = data_dict['properties']['Categories']['multi_select']
    markdown.append("- **Categories** (multi_select):")
    for category in categories:
        markdown.append(f"  - {category['name']} ({category['color']})")
    markdown.append(f"- **Status** (status): {data_dict['properties']['Status']['status']['name']}")
    markdown.append(f"- **List** (select): {data_dict['properties']['List']['select']}")
    markdown.append(f"- **Title** (title): {data_dict['properties']['Title']['title'][0]['plain_text']}")

    # Content
    markdown.append("\n## Content")
    for item in data_list:
        for key, value in item.items():
            if key == 'heading_1':
                markdown.append(f"- ### Heading 1\n  - {value['rich_text'][0]['text']['content']}")
            elif key == 'bulleted_list_item':
                if not markdown[-1].startswith("- ### Bulleted List"):
                    markdown.append("- ### Bulleted List")
                markdown.append(f"  - {value['rich_text'][0]['text']['content']}")
            elif key == 'numbered_list_item':
                if not markdown[-1].startswith("- ### Numbered List"):
                    markdown.append("- ### Numbered List")
                markdown.append(f"  - {value['rich_text'][0]['text']['content']}")

    return "\n".join(markdown)

import re

def markdown_to_list_dict(markdown):
    lines = markdown.split('\n')
    data_dict = {}
    data_list = []

    # Initialize placeholders for data_dict
    properties = {
        'Notes': {'id': '%3C%5DID', 'type': 'relation', 'relation': [], 'has_more': False},
        'Categories': {'id': 'MRFH', 'type': 'multi_select', 'multi_select': []},
        'Status': {'id': 'jTpO', 'type': 'status', 'status': {'id': '', 'name': '', 'color': 'default'}},
        'List': {'id': 'wLtb', 'type': 'select', 'select': None},
        'Title': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': '', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '', 'href': None}]}
    }

    # Parse lines
    for line in lines:
        if line.startswith("# Notion Page: "):
            title = line.replace("# Notion Page: ", "").strip()
            properties['Title']['title'][0]['plain_text'] = title
            properties['Title']['title'][0]['text']['content'] = title
        elif line.startswith("- **ID**: "):
            data_dict['id'] = line.replace("- **ID**: ", "").strip()
        elif line.startswith("- **Created Time**: "):
            data_dict['created_time'] = line.replace("- **Created Time**: ", "").strip()
        elif line.startswith("- **Last Edited Time**: "):
            data_dict['last_edited_time'] = line.replace("- **Last Edited Time**: ", "").strip()
        elif line.startswith("- **Created By**: "):
            data_dict['created_by'] = {'object': 'user', 'id': line.replace("- **Created By**: ", "").strip()}
        elif line.startswith("- **Last Edited By**: "):
            data_dict['last_edited_by'] = {'object': 'user', 'id': line.replace("- **Last Edited By**: ", "").strip()}
        elif line.startswith("- **Parent Database ID**: "):
            data_dict['parent'] = {'type': 'database_id', 'database_id': line.replace("- **Parent Database ID**: ", "").strip()}
        elif line.startswith("- **Archived**: "):
            data_dict['archived'] = line.replace("- **Archived**: ", "").strip() == 'True'
        elif line.startswith("- **In Trash**: "):
            data_dict['in_trash'] = line.replace("- **In Trash**: ", "").strip() == 'True'
        elif line.startswith("- **URL**: "):
            url_match = re.search(r"\((.*?)\)", line)
            data_dict['url'] = url_match.group(1) if url_match else ""
        elif line.startswith("  - "):
            category_match = re.search(r"\- (.*?) \((.*?)\)", line)
            if category_match:
                properties['Categories']['multi_select'].append({'id': '', 'name': category_match.group(1), 'color': category_match.group(2)})
        elif line.startswith("- **Status** (status): "):
            properties['Status']['status']['name'] = line.replace("- **Status** (status): ", "").strip()
        elif line.startswith("- **List** (select): "):
            properties['List']['select'] = line.replace("- **List** (select): ", "").strip()
        elif line.startswith("- ### Heading 1"):
            heading_content = lines[lines.index(line) + 1].replace("  - ", "").strip()
            data_list.append({'heading_1': {'rich_text': [{'text': {'content': heading_content}}]}})
        elif line.startswith("- ### Bulleted List"):
            i = lines.index(line) + 1
            while i < len(lines) and lines[i].startswith("  - "):
                bulleted_content = lines[i].replace("  - ", "").strip()
                data_list.append({'bulleted_list_item': {'rich_text': [{'text': {'content': bulleted_content}}]}})
                i += 1
        elif line.startswith("- ### Numbered List"):
            i = lines.index(line) + 1
            while i < len(lines) and lines[i].startswith("  - "):
                numbered_content = lines[i].replace("  - ", "").strip()
                data_list.append({'numbered_list_item': {'rich_text': [{'text': {'content': numbered_content}}]}})
                i += 1

    data_dict['properties'] = properties
    return data_list, data_dict