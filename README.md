Text analyzer that uses Optical Character Recognition (OCR) to detect text from handwritten notes and turns notes into a Notion page

General Implementation Idea:
- [x] OCR with Azure AI Vision SDK
- [x] parses detected text into a text file
- [ ] uses regex to identify each line
    # example: identify numbered lists -> '[0-9]\.\s'
    # example: identify bullet_list -> '^-.+'

- [ ] organize information into a dictionary
    #  page = {[
    #    'numbered_list': [numbered list text],
    #    'bullet_list': [text.split('-')],
    #    'nested_list': [
    #       {
    #           parent_text: "some text",
    #           children: ["blah", "bleep", "bloop"]
    #       }
    #    ]
    # ]}
    
- [ ] uses data from dictionary to create notion document using Notion API
