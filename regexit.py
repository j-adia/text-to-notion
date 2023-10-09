import re
from dotenv import load_dotenv
import os
from notion_client import AsyncClient

text = '''TO-DO:
1. Meal prep over-night oats for breakfast
2. Prepare for morning lab
3. Fold laundry
4. Practice code'''

# find numbered list (1. ) in text 
match = re.compile('[0-9]\.\s.*')
matches = match.findall(text)

# array to hold our numbered list elements
numbered_list = []

# extract list item's number and text
for i in range(0, len(matches)):
    numbered_list_item = {'list_item_number': 0, 'text': ""}
    list_item_number = matches[i].split('.')[0]
    list_item_text = matches[i].split('.')[1]
    numbered_list_item['list_item_number']  = list_item_number
    numbered_list_item['text'] = list_item_text.lstrip()
    numbered_list.append(numbered_list_item)

print(numbered_list)




