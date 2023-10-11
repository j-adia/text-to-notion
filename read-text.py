from ocr_imports import *

def main():
    global cv_client
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Menu for text reading functions
        print('Pick a number to show example\n'
              '1: To-do List\n2: Health and Fitness Log\n'
              '3: Class Notes\n4: Dog Notes\n'
              '5: Weekly Activity Tracker')
        command = input('Enter a number: ')

        if command == '1':
            image_file = os.path.join('images', 'note1.jpg')
            GetTextRead(image_file)
        elif command == '2':
            image_file = os.path.join('images', 'bj.png')
            GetTextRead(image_file)
        elif command == '3':
            image_file = os.path.join('images', 'note2.jpg')
            GetTextRead(image_file)
        elif command == '4':
            image_file = os.path.join('images', 'note3.jpg')
            GetTextRead(image_file)
        elif command == '5':
            image_file = os.path.join('images', 'note4.jpg')
            GetTextRead(image_file)

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('Reading text in {}\n'.format(image_file))

    # Use Read API to read text in image
    with open(image_file, mode="rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)

        # Get the async operation ID so we can check for the results
        operation_location = read_op.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the asynchronous operation to complete
        while True:
            read_results = cv_client.get_read_result(operation_id)
            if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)

        # If the operation was successful, process the text line by line
        if read_results.status == OperationStatusCodes.succeeded:
            print("Copying results to text file...")

            # writes analyzed results to text file line by line
            with open('detected_text.txt', mode='w') as file:
                for page in read_results.analyze_result.read_results:
                    for line in page.lines:
                        file.write(line.text + '\n')
            print("Text file generated")            
            file.close()
            

if __name__ == "__main__":
    main()
