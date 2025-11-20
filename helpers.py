from pathlib import Path

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
