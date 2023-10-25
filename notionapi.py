# put imports into a separate python file to make the page prettier 😄
from api_imports import *

# -------------------------------
# using regex to segment our text file into numbered list and bullet point 

import re
try:
    with open('detected_text.txt') as file:
        line = file.read()
        # find numbered list (1. ) 
        m = re.findall('\d+\.\s+.*', line)
        # find bullet point list -, *, 
        p = re.findall('(\n\-|\*)(\s.*)', line)

    file.close()

except FileNotFoundError:
    print('file was not found!')

# array to hold numbered list items
numberlist = []

for match in m:
    # argument '1' ensures splitting is done only one time
    numberlist.append(match.split('.', 1)[1].lstrip())

print(numberlist)

# array to hold bullet list items
bulletlist = []

for match in p:
    bulletlist.append(match[1].lstrip())

print(bulletlist)
# -------------------------------


# -------------------------------
# using notion-client (notion API) to create/append pages

# get the notion token from the .env file
load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN')) 

# get the 'master page' id
page_id = os.getenv('PAGE_ID')
new_page_id = []

# creating a new page:
# things to note:
#   - do not capitalize page properties, results in API response error: "Invalid property identifier"
#   - when creating a new page, the only property that can be accessed is 'title'

# array that holds page content blocks
page_content = [
    {"heading_2":{"rich_text":[{"text":{"content": "Numbered List from text file:"}}]}}
]

for item in numberlist:
    page_content.append({"numbered_list_item":{"rich_text":[{"text":{"content": item}}]}})

for item in bulletlist:
    page_content.append({"bulleted_list_item":{"rich_text":[{"text":{"content": item}}]}})

# adds a new page block to parent page
def create_page():
    print("CREATE NEW PAGE")

    your_title = input("enter a new page title: ")

    properties = {
        "title": [{"text": {"content": your_title}}],  
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
        notion.blocks.children.append(block_id=new_page_id[0], children=content
            # SAMPLE BLOCK STRUCTURE
            # [
            #     {"heading_2":{"rich_text":[{"text":{"content": "a bot made this page!"}}]}},
            #     {"paragraph":{"rich_text":[{"text":{"content": "How?"}}]}},
            #     {"toggle":{"rich_text":[{"text":{"content": "a developer made a program in python"}}]}},
            # ]
        )
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

