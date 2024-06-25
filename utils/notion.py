import re
import json

def create_equation(expression):
    return {
        "type": "equation",
        "equation": {
            "expression": expression
        },
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default"
        },
        "plain_text": expression,
        "href": None
    }

def create_notion_block(content, block_type='paragraph'):
    if block_type == 'equation':
        # Equation block requires 'expression' instead of 'rich_text'
        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "expression": content
            }
        }
    elif block_type in ['code', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item', 'quote', 'image', 'divider']:
        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"text": {"content": content if isinstance(content, str) else "\n".join(content)}}]
            }
        }
    else:
        # This is for normal text and inline code
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": content}}] if isinstance(content, str) else content
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
        if block_latex_regex.search(line):
            latex_content = block_latex_regex.findall(line)[0].strip()
            notion_blocks.append(create_notion_block(latex_content, 'equation'))
            continue

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
            # Inline code, links, images, and inline LaTeX
            rich_text_list = []
            # Split line into normal text and LaTeX parts
            parts = re.split(inline_latex_regex, line)
            is_latex = False  # Track whether the next part is LaTeX

            for part in parts:
                if is_latex:
                    rich_text_list.append(create_equation(part))
                else:
                    # Process normal text for links and images
                    part = re.sub(link_regex, lambda match: f"{match.group(1)} (URL: {match.group(2)})", part)
                    part = re.sub(image_regex, lambda match: f"Image: {match.group(1)} (URL: {match.group(2)})", part)
                    if part.startswith('`') and part.endswith('`'):
                        rich_text_list.append(create_rich_text(part[1:-1], is_code=True))
                    else:
                        rich_text_list.append(create_rich_text(part))
                is_latex = not is_latex

            if rich_text_list:
                notion_blocks.append(create_notion_block(rich_text_list, 'paragraph'))


    # Check for unclosed code block at the end of text
    if code_block:
        notion_blocks.append(create_notion_block(code_content, 'code'))

    return notion_blocks