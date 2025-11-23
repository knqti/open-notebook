from pathlib import Path
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f'{self.base_url}{endpoint}', params=params)
        return response.json()
    
    def post_data(self, endpoint, data=None, files=None):
        response = requests.post(f'{self.base_url}{endpoint}', data=data, files=files)
        return response.json()
    
    def post_json(self, endpoint, json=None, files=None):
        response = requests.post(f'{self.base_url}{endpoint}', json=json, files=files)
        return response.json()

def confirm_upload_dir(directory) -> object:
    user_input = input(f'Files to be uploaded are in "{directory}" (y/n): ')
    
    if user_input.lower().strip() != 'y':
        directory = Path(input('Enter the correct directory: '))

    return directory

def extract_notebook_id(notebooks: list, existing_notebook_names: list) -> str:
    # Check if notebook exists
    print('\nEnter the notebook name:')
    for name in existing_notebook_names:
        print(name)
    
    target_notebook_name = input('>> ').strip()
    existing_set = set(existing_notebook_names)
    
    if target_notebook_name not in existing_set:
        print(f'ERROR: notebook title {target_notebook_name} not found')
        raise Exception
    
    # Extract notebook id
    for notebook in notebooks:
        if target_notebook_name == notebook['name']:
            notebook_id = notebook['id']
    # notebook_id = [notebook['id'] for notebook in notebooks if target_notebook_name == notebook['name']]
            # print(f'Extracted notebook ID: {notebook_id}')
            return notebook_id 

def upload_sources(api_client, directory, existing_sources, target_notebook_id):
    existing_set = set(existing_sources)

    for file in directory.iterdir():
        if file.name in existing_set:
            continue

        with open(file, 'rb') as f:

            source_metadata = {
                'type': 'upload',
                'notebook_id': target_notebook_id,
                'title': file.name,
                'embed': True,
                'delete_source': False,
                'async_processing': True
            }

            response = api_client.post_data(
                endpoint='/api/sources',
                data=source_metadata,
                files={'file': f}
            )

            print(f'Posted source "{response['title']}" with ID "{response['id']}"')

def create_insight(api_client, source_id, transformation_id, model_id):
    response = api_client.post_json(
        endpoint=f'/api/sources/{source_id}/insights', 
        json={
            'transformation_id': transformation_id,
            'model_id': model_id
        }
    )

    print(f'Posted transformation insight "{response['insight_type']}" on source ID "{response['source_id']}"')
    