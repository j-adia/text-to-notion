Text analyzer that uses Optical Character Recognition (OCR) to detect text from handwritten notes and turns notes into a Notion page

General Implementation Idea:
- [x] OCR with Azure AI Vision SDK
- [x] parses detected text into a text file
- [x] uses regex to identify each line
- [x] organize information into a dictionary
- [x] uses data from dictionary to create notion document using Notion API

Next Steps:

Tweaks:
- [ ] make function to detect and add nested block elements
- [ ] find a tool that cleans up spelling errors by Read API 

Bugs:
- [ ] when a bullet point has text spanning more than one line, only the first line is parsed as a bullet point, while the remaining lines are separated and parsed as paragraphs

Major Stuff:
- [ ] make web app for project:
    - [x] make page layout
    - [ ] make a drag and drop file box
    - [ ] add javascript
        - [ ] make a transition from landing page to drag and drop box

