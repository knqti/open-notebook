import json
import requests
from pathlib import Path

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f'{self.base_url}{endpoint}', params=params)
        return response.json()
    
    def post(self, endpoint, data=None, files=None):
        response = requests.post(f'{self.base_url}{endpoint}', data=data, files=files)
        return response.json()
    
def confirm_upload_dir(directory) -> object:
    user_input = input(f'Files to be uploaded are in "{directory}" (y/n): ')
    
    if user_input.lower().strip() != 'y':
        directory = Path(input('Enter the correct directory: '))

    return directory

def extract_notebook_id(notebooks: list, existing_notebook_names: list) -> str:
    # Check if notebook exists
    target_notebook_name = input('Enter the notebook name: ').strip()
    existing_set = set(existing_notebook_names)
    
    if target_notebook_name not in existing_set:
        print(f'ERROR: notebook title {target_notebook_name} not found')
        raise Exception
    
    # Extract notebook id
    for notebook in notebooks:
        if target_notebook_name == notebook['name']:
            notebook_id = notebook['id']
    # notebook_id = [notebook['id'] for notebook in notebooks if target_notebook_name == notebook['name']]
            print(f'Extracted notebook ID: {notebook_id}')
            return notebook_id 

def create_transformations_dict(transformations: list, existing_transformation_names: list) -> dict:
    transformations_dict = {}

    for name in existing_transformation_names:

        for item in transformations:
            if item['name'] == name:
                transformations_dict[name] = item['id']
                break

    # print(f'Created transformations dictionary: {transformations_dict}')
    return transformations_dict

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

            response = api_client.post(
                endpoint='/api/sources',
                data=source_metadata,
                files={'file': f}
            )

            print(f'Called API to post new source: {file.name}\nResponse: {response}')


if __name__ == '__main__':
    client = APIClient('http://localhost:5055')
    root_dir = Path(__file__).parent

    # Notebooks
    notebooks = client.get(endpoint='/api/notebooks')
    existing_notebook_names = [notebook['name'] for notebook in notebooks]
    target_notebook_id = extract_notebook_id(notebooks, existing_notebook_names)
    
    # Transformations
    # transformations = client.get(endpoint='/api/transformations')
    # transformation_names = [
    #     'Analyze Paper',
    #     'Dense Summary',
    #     'Key Insights',
    #     'Reflections',
    #     'Simple Summary',
    #     'Table of Contents'
    # ]
    # transformations_dict = create_transformations_dict(transformations, transformation_names)

    # Sources
    sources = client.get(endpoint='/api/sources')
    sources_dir = confirm_upload_dir(root_dir / 'sources_to_upload')
    existing_source_titles = [source['title'] for source in sources]
    
    upload_sources(
        client,
        sources_dir,
        existing_source_titles,
        target_notebook_id
    )    
