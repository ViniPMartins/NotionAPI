from scripts import *

if __name__ == '__main__':

    data = get_data_Notion_API()
    new_query_API = transform_API_data(data)
    
    try:
        saved_query = load_save_json()
    except FileNotFoundError:
        save_new_json(new_query_API)
        saved_query = load_save_json()

    verify_modifications(new_query_API, saved_query)