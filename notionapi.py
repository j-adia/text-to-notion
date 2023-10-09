from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import requests
import json


# using Notion API

# token authentication
load_dotenv()
notion_token = os.getenv('NOTION_TOKEN')
page_id = os.getenv('PAGE_ID')

headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# gets all 'paragraph' blocks on page
def get_page_content():
    # make a request to Notion API endpoint
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    r = requests.get(url, headers=headers)

    # organize the data given from the request into a dictionary
    data_dict = r.json()
    print(json.dumps(data_dict, indent=2))

    # loop through each content block in the 'results' array
    for block in data_dict["results"]:
        # get text
        page_text = block["paragraph"]["rich_text"][0]["plain_text"]
        print(page_text)

def append_page():
    pass


def create_page(data: dict):
    pass