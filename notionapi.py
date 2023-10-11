# put imports into a separate python file to make the page prettier 😄
from api_imports import *

# get the notion token from the .env file
load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN')) 
page_id = os.getenv('PAGE_ID')

# creating a new page:
# things to note:
#   - do not capitalize page properties, results in API response error: "Invalid property identifier"
#   - all arguments must be objects
#   - when creating a new page, the only property that can be accessed is 'title'

# adds a new page to your notion page
print("CREATE NEW PAGE")

your_title = input("enter a new page title: ")

properties = {
    "title": [{"text": {"content": your_title}}],  
}

notion.pages.create(parent=page_id, properties=properties)

# get page URL
page = notion.pages.retrieve(page_id=page_id)
print(json.dumps(page,indent=2))
link = page['url']
print("page link => " + link)


















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

