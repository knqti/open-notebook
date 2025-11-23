from pathlib import Path
from api_helpers import (
    APIClient,
    confirm_upload_dir,
    extract_notebook_id,
    upload_sources,
    create_insight
)
    

if __name__ == '__main__':
    client = APIClient('http://localhost:5055')
    root_dir = Path(__file__).parent

    # Check API
    try:
        response = client.get('/')
        print(f'API OK: {response['message']}')
    except Exception as e:
        print(f'ERROR --- API init failed: {e}')

     # Get notebooks
    notebooks = client.get(endpoint='/api/notebooks')
    existing_notebook_names = [notebook['name'] for notebook in notebooks]
    
    # Get sources
    sources = client.get(endpoint='/api/sources')
    existing_source_titles = [source['title'] for source in sources]

   # Get transformations
    transformations = client.get(endpoint='/api/transformations')

    # Get models
    models = client.get(endpoint='/api/models')

    # User input
    print(
    '''
    \nEnter a number to choose:
    1) Upload sources
    2) Create insights
    3) Exit
    '''
    )
    user_input = input('>> ').strip()

    # Upload sources
    if user_input == '1':
        sources_dir = confirm_upload_dir(root_dir / 'sources_to_upload')
        target_notebook_id = extract_notebook_id(notebooks, existing_notebook_names)

        upload_sources(
            client,
            sources_dir,
            existing_source_titles,
            target_notebook_id
        )

        print('Done!')

    # Create insights
    elif user_input == '2':
        source_title_id = {}
        for source_item in sources:
            source_title_id[source_item['title']] = source_item['id']

        trfrms_name_id = {}
        for trfrms_item in transformations:
            trfrms_name_id[trfrms_item['name']] = trfrms_item['id']

        model_name_id = {}
        for model_item in models:
            model_name_id[model_item['name']] = model_item['id']
        
        print('\nEnter a source ID:')
        for key, value in sorted(source_title_id.items()):
            print(f'{key}: {value}')
        source_id = input('>> ').strip()

        print('\nEnter a transformation ID:')
        for key, value in sorted(trfrms_name_id.items()):
            print(f'{key}: {value}')
        transformation_id = input('>> ').strip()

        print('\nEnter a model ID:')
        for key, value in sorted(model_name_id.items()):
            print(f'{key}: {value}')
        model_id = input('>> ').strip()

        insight_results = create_insight(client, source_id, transformation_id, model_id)

        print('Done!')

    # Exit
    else:
        print('Exiting...goodbye')
