import re

def create_notion_block(content_list, block_type='paragraph'):
    if block_type in ['code', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item', 'quote', 'image', 'divider']:
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
    inline_latex_regex = re.compile(r'\$(.*?)\$')
    block_latex_regex = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
    code_block = False
    code_content = []

    for line in lines:
        if line.startswith('```'):
            if code_block:
                notion_blocks.append(create_notion_block(code_content, 'code'))
                code_block = False
                code_content = []
            else:
                code_block = True
            continue

        if code_block:
            code_content.append(line)
            continue

        if not line.strip():
            continue
        
        if block_latex_regex.search(line):
            # Extract and process block LaTeX
            latex_content = block_latex_regex.findall(line)[0].strip()
            notion_blocks.append(create_notion_block(latex_content, 'equation'))
            continue

        # Headings, lists, quotes
        if line.startswith('# '):
            notion_blocks.append(create_notion_block(line[2:], 'heading_1'))
        elif line.startswith('## '):
            notion_blocks.append(create_notion_block(line[3:], 'heading_2'))
        elif line.startswith('### '):
            notion_blocks.append(create_notion_block(line[4:], 'heading_3'))
        elif line.startswith('- '):
            notion_blocks.append(create_notion_block(line[2:], 'bulleted_list_item'))
        elif re.match(r'\d+\. ', line):
            notion_blocks.append(create_notion_block(line[line.find('. ')+2:], 'numbered_list_item'))
        elif line.startswith('> '):
            notion_blocks.append(create_notion_block(line[2:], 'quote'))
        elif line.startswith('---'):
            notion_blocks.append(create_notion_block("", 'divider'))
        else:
            # Inline code, links, images
            rich_text_list = []
            parts = re.split(r'(`[^`]*`)', line)  # Split line into parts for normal text and inline code
            for part in parts:
                if part.startswith('`') and part.endswith('`'):
                    rich_text_list.append(create_rich_text(part[1:-1], is_code=True))
                else:
                    # Handle links and images in normal text parts
                    part = re.sub(link_regex, lambda match: f"{match.group(1)} (URL: {match.group(2)})", part)
                    part = re.sub(image_regex, lambda match: f"Image: {match.group(1)} (URL: {match.group(2)})", part)
                    rich_text_list.append(create_rich_text(part))
            if rich_text_list:
                notion_blocks.append(create_notion_block(rich_text_list))

    # Check for unclosed code block at the end of text
    if code_block:
        notion_blocks.append(create_notion_block(code_content, 'code'))

    return notion_blocks
