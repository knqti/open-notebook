import json
import requests
from pathlib import Path
from helpers import (
    confirm_upload_dir,
    create_transformations_dict,
    extract_notebook_id,
    upload_sources
)

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f'{self.base_url}{endpoint}', params=params)
        return response.json()
    
    def post(self, endpoint, data=None, files=None):
        response = requests.post(f'{self.base_url}{endpoint}', data=data, files=files)
        return response.json()
    

if __name__ == '__main__':
    client = APIClient('http://localhost:5055')
    root_dir = Path(__file__).parent

    # Check API
    try:
        response = client.get('/')
        response.raise_for_status()
        print(f'API OK: {response.status_code}')
    except Exception as e:
        print(f'ERROR --- API init failed: {e}')

    # Get transformations
    transformations = client.get(endpoint='/api/transformations')
    transformation_names = [
        'Analyze Paper',
        'Dense Summary',
        'Key Insights',
        'Reflections',
        'Simple Summary',
        'Table of Contents'
    ]
    existing_transformations_dict = create_transformations_dict(transformations, transformation_names)

    # Get notebooks
    notebooks = client.get(endpoint='/api/notebooks')
    existing_notebook_names = [notebook['name'] for notebook in notebooks]
    
    # Get sources
    sources = client.get(endpoint='/api/sources')
    sources_dir = confirm_upload_dir(root_dir / 'sources_to_upload')
    existing_source_titles = [source['title'] for source in sources]
    


    target_notebook_id = extract_notebook_id(notebooks, existing_notebook_names)

    upload_sources(
        client,
        sources_dir,
        existing_source_titles,
        target_notebook_id
    )
