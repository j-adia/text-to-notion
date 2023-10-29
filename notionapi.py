# put imports into a separate python file to make the page prettier 😄
from api_imports import *

# -------------------------------
# using notion-client (notion API) to create/append pages

# get the notion token from the .env file
load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN')) 

# get the 'master page' id
page_id = os.getenv('PAGE_ID')

# array that holds page content blocks
page_content = [
    # {"heading_2":{"rich_text":[{"text":{"content": "Numbered List from text file:"}}]}}
]

# -------------------------------
# using regex to parse our text file and find numbered list, bulleted list, paragraph, and header

import re

# keep the title of our file to use later
page_title = []

try:
    with open('detected_text.txt', 'r') as file:
        # CASE: what if there was an empty line in front of the title?
        # find title (first line in text starts with a word)
        title = re.search(r'^[a-z].*', file.readline(), re.IGNORECASE)
        if (title):
            text = title.group()
            page_title.append(text)
            page_content.append({"heading_1":{"rich_text":[{"text":{"content": text}}]}})

        # used as a flag when we encounter an empty space (used to catch headings)
        empty_space = None

        for line in file:   
            # when the previous line is empty, the line after is a heading       
            if (empty_space):
                text = line
                page_content.append({"heading_3":{"rich_text":[{"text":{"content": text}}]}})
                empty_space = None
                continue

            # find numbered list (1. ) 
            n = re.search(r'\d+\s*\.\s+.*', line)
            # find bullet point list -, *, 
            b = re.search(r'(\n?\-|\*)(\s.*)', line)
            # find paragraph
            p = re.search(r'^[a-z].*', line, re.IGNORECASE)
            # find empty space 
            empty_space = re.search(r'^\s*$', line)
            print(empty_space)

            if (empty_space):
                # proceed to next line
                continue

            if (n):
                # argument '1' ensures splitting is done only one time
                text = n.group().split('.', 1)[1].lstrip()
                page_content.append({"numbered_list_item":{"rich_text":[{"text":{"content": text}}]}})

            if (b):
                text = b.group(2).lstrip()
                page_content.append({"bulleted_list_item":{"rich_text":[{"text":{"content": text}}]}})

            if (p):
                text = p.group()
                page_content.append({"paragraph":{"rich_text":[{"text":{"content": text}}]}})
            
    file.close()

except FileNotFoundError:
    print('file was not found!')
# -------------------------------

# creating a new page:
# things to note:
#   - do not capitalize page properties, results in API response error: "Invalid property identifier"
#   - when creating a new page, the only property that can be accessed is 'title'

# adds a new page block to parent page
new_page_id = []

def create_page():
    print("CREATE NEW PAGE")

    if (not title):
        text = input("enter a page title: ")
        page_title.append(text)

    properties = {
        "title": [{"text": {"content": page_title[0]}}],  
    }

    # create new page request from Notion API
    try:
        new_page = notion.pages.create(parent={'page_id':page_id}, properties=properties)
    except Exception as e:
        print(e)

    print(f"\nnew page \"{new_page['properties']['title']['title'][0]['text']['content']}\" successfully created!")
    # print(json.dumps(new_page,indent=2))

    # save new page ID + print URL
    new_page_id.append(new_page["id"])
    new_page_url = new_page["url"]
    print(f"\nnew page ID: {new_page_id}\npage URL: {new_page_url}")

# add new content blocks to page
def add_content(content):
    try:
        notion.blocks.children.append(block_id=new_page_id[0], children=content)
        print(json.dumps(content, indent=2))
    except Exception as e:
        print(e)

create_page()
add_content(page_content)














# token authentication

# notion_token = os.getenv('NOTION_TOKEN')
# page_id = os.getenv('PAGE_ID')

# headers = {
#     "Authorization": f"Bearer {notion_token}",
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28",
# }

# gets all 'paragraph' blocks on page
# def get_page_content():
#     # make a request to Notion API endpoint
#     url = f"https://api.notion.com/v1/blocks/{page_id}/children"
#     r = requests.get(url, headers=headers)

#     # organize the data given from the request into a dictionary
#     data_dict = r.json()
#     print(json.dumps(data_dict, indent=2))

#     # loop through each content block in the 'results' array
#     for block in data_dict["results"]:
#         # get text
#         page_text = block["paragraph"]["rich_text"][0]["plain_text"]
#         print(page_text)

