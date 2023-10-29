# put imports into a separate python file to make the page prettier 😄
from api_imports import *

def main():
    # if there is an issue running read_text.py, exit program
    try:
        subprocess.run(['python', 'read_text.py'], check=True, text=True)

    except subprocess.CalledProcessError as e:
        sys.exit(1)

    # get the notion token from the .env file
    load_dotenv()
    notion = Client(auth=os.getenv('NOTION_TOKEN')) 

    # get the 'master page' id
    page_id = os.getenv('PAGE_ID')

    new_page_id = []
    page_title = []

    # array that holds page content blocks
    page_content = [
        # {"heading_2":{"rich_text":[{"text":{"content": "Numbered List from text file:"}}]}}
        {"divider":{}}
    ]

    parse_file(page_title, page_content)
    create_page(page_title, page_id, new_page_id, notion)
    add_content(new_page_id, page_content, notion)



# deletes our text file after we're done using it
def delete_text_file():
    try:
        os.remove('detected_text.txt')
        print("Discarded text file\n")
    except Exception as e:
        print(f"Warning: text file could not be deleted\n{e}")

# adds a new line to page
def new_line(page_content):
    page_content.append({"paragraph":{"rich_text":[{"text":{"content": " "}}]}})

# uses regex to parse our text file and find title, numbered list, bulleted list, paragraph, header, etc.
def parse_file(page_title, page_content):
    print("\nParsing text file...")
    time.sleep(1)

    try:
        with open('detected_text.txt', 'r') as file:
            # find title (first line in text starts with a word)
            title = re.search(r'^[a-z].*', file.readline(), re.IGNORECASE)
            if (title):
                text = title.group()
                page_title.append(text)
                new_line(page_content)

            # used as a flag when we encounter an empty space (used to catch headings)
            empty_space = None

            for line in file:   
                # when the previous line is empty, the line after is a heading       
                if (empty_space):
                    text = line
                    new_line(page_content)
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
        print("Parsing complete!")
        delete_text_file()

    except FileNotFoundError as e:
        print(e)
        exit(1)

# notion-client module: create/append pages

# adds a new page block to parent page
def create_page(page_title, page_id, new_page_id, notion: Client):
    if (not page_title):
        text = input("\nNo title was detected, enter a new page title: ")
        page_title.append(text)

    properties = {
        "title": [{"text": {"content": page_title[0]}}],  
    }

    print("Creating new page...")

    # create new page request from Notion API
    try:
        new_page = notion.pages.create(parent={'page_id':page_id}, properties=properties)
    except Exception as e:
        print(e)

    print(f"New page \"{new_page['properties']['title']['title'][0]['text']['content']}\" successfully created!")
    # print(json.dumps(new_page,indent=2))

    # save new page ID + print URL
    print("\nNew Page Info:")
    new_page_id.append(new_page["id"])
    new_page_url = new_page["url"]
    print(f"Page ID: {new_page_id}\nPage URL: {new_page_url}")

# add new content blocks to page
def add_content(new_page_id, content: dict, notion: Client):
    try:
        notion.blocks.children.append(block_id=new_page_id[0], children=content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
