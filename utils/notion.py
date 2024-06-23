import json
import re

def create_notion_block(block_type, content, url=None, language='plaintext'):
    if block_type == 'code':
        return {
            "code": {
                "rich_text": [{"text": {"content": content}}],
                "language": language
            }
        }
    elif url:
        return {
            block_type: {
                "rich_text": [{
                    "text": {
                        "content": content,
                        "link": {"url": url}
                    }
                }]
            }
        }
    else:
        return {
            block_type: {
                "rich_text": [{"text": {"content": content}}]
            }
        }
  
def markdown_to_notion(md_text):
    notion_blocks = []
    lines = md_text.split('\n')
    md_to_notion = {
        '# ': ('heading_1', None),
        '## ': ('heading_2', None),
        '### ': ('heading_3', None),
        '- ': ('bulleted_list_item', None),
        '1. ': ('numbered_list_item', None),
        '> ': ('quote', None),
        '```': ('code', None)
    }
    link_regex = re.compile(r'$begin:math:display$(.*?)$end:math:display$$begin:math:text$(.*?)$end:math:text$')
    image_regex = re.compile(r'!$begin:math:display$(.*?)$end:math:display$$begin:math:text$(.*?)$end:math:text$')
    code_block = False
    code_content = []

    for line in lines:
        if code_block:
            if line == '```':
                notion_blocks.append(create_notion_block('code', '\n'.join(code_content), language='python'))
                code_block = False
                code_content = []
            else:
                code_content.append(line)
            continue
        for md_symbol, (block_type, _) in md_to_notion.items():
            if line.startswith(md_symbol):
                content = line[len(md_symbol):]
                if block_type == 'code' and line == '```':
                    code_block = True
                    break
                notion_blocks.append(create_notion_block(block_type, content))
                break
        else:
            notion_blocks.append(create_notion_block('paragraph', line))

    return notion_blocks