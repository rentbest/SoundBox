import sys
import requests

BASE_URL = 'http://127.0.0.1:8888'


def upload(file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(f'{BASE_URL}/upload', files=files)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error uploading file: {response.text}")


def list_files():
    response = requests.get(f'{BASE_URL}/uploads')
    if response.status_code == 200:
        files = response.json().get('files', [])
        for file in files:
            print(file)
    else:
        print(f"Error listing files: {response.text}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:')
        print('python screwdriver.py upload /path/to/file.mp3')
        print('python screwdriver.py list')
        sys.exit(1)

    action = sys.argv[1]

    if action == 'upload':
        if len(sys.argv) < 3:
            print('Please provide the path to the audio file.')
            sys.exit(1)
        file_path = sys.argv[2]
        upload(file_path)

    elif action == 'list':
        list_files()

    else:
        print('Invalid action. Use "upload" or "list".')
        sys.exit(1)
