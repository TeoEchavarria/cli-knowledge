import json
import re

def create_notion_block(content_list, block_type='paragraph'):
    if block_type in ['code', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item', 'quote']:
        return {
            block_type: {
                "rich_text": [{"text": {"content": content_list if isinstance(content_list, str) else "\n".join(content_list)}}]
            }
        }
    else:
        # This is for normal text and inline code
        return {
            "paragraph": {
                "rich_text": content_list
            }
        }

def create_rich_text(content, is_code=False, url=None):
    text_structure = {"text": {"content": content}}
    if url:
        text_structure["text"]["link"] = {"url": url}
    if is_code:
        text_structure["annotations"] = {"code": True}
    return text_structure

def markdown_to_notion(md_text):
    notion_blocks = []
    lines = md_text.split('\n')
    link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    image_regex = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    code_block = False
    code_content = []

    for line in lines:
        if line.startswith('```'):
            if code_block:
                # End of code block
                notion_blocks.append(create_notion_block(code_content, 'code'))
                code_block = False
                code_content = []
            else:
                # Start of code block
                code_block = True
            continue

        if code_block:
            code_content.append(line)
            continue

        if not line.strip():
            continue

        if line.startswith('# '):
            notion_blocks.append(create_notion_block(line[2:], 'heading_1'))
            continue
        elif line.startswith('## '):
            notion_blocks.append(create_notion_block(line[3:], 'heading_2'))
            continue
        elif line.startswith('### '):
            notion_blocks.append(create_notion_block(line[4:], 'heading_3'))
            continue
        elif line.startswith('- '):
            notion_blocks.append(create_notion_block(line[2:], 'bulleted_list_item'))
            continue
        elif re.match(r'\d+\. ', line):
            notion_blocks.append(create_notion_block(line[line.find('. ')+2:], 'numbered_list_item'))
            continue
        elif line.startswith('> '):
            notion_blocks.append(create_notion_block(line[2:], 'quote'))
            continue

        rich_text_list = []
        parts = re.split(r'(`[^`]*`)', line)  # Split line into parts for normal text and inline code
        for part in parts:
            if part.startswith('`') and part.endswith('`'):
                code_text = part[1:-1]
                rich_text_list.append(create_rich_text(code_text, is_code=True))
            else:
                # Handle links and images in normal text parts
                part = re.sub(link_regex, lambda match: f"{match.group(1)} (URL: {match.group(2)})", part)
                part = re.sub(image_regex, lambda match: f"Image: {match.group(1)} (URL: {match.group(2)})", part)
                rich_text_list.append(create_rich_text(part))

        if rich_text_list:
            notion_blocks.append(create_notion_block(rich_text_list))

    # Check for unclosed code block at end of text
    if code_block:
        notion_blocks.append(create_notion_block(code_content, 'code'))

    return notion_blocks