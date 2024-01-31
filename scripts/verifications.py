import json
from get_data_api import get_data_Notion_API, transform_API_data

def save_new_json(dict_json):
    print("Salvando novo JSON")
    json_object = json.dumps(dict_json)
    with open("status_atual_projetos.json", 'w') as file:
        file.write(json_object)
    return True

def load_save_json():
    with open("./status_atual_projetos.json", 'r') as file:
        file_json = file.read()
        dict_json = json.loads(file_json)
    return dict_json

def verify_new_project(new_query_API, saved_query):
    new_project = False
    list_new_project = []

    for id in new_query_API['project_ID']:
        if id not in saved_query['project_ID']:
            new_project = True
            list_new_project.append(id)
    
    return (new_project, list_new_project)

def verify_delete_project(new_query_API, saved_query):
    delete_project = False
    list_deleted_project = []

    for id in saved_query['project_ID']:
        if id not in new_query_API['project_ID']:
            delete_project = True
            list_deleted_project.append(id)
    
    return (delete_project, list_deleted_project)

def verify_status_change_project(new_query_API, saved_query):
    status_change = False
    list_status_change_project = []

    for idx, id in enumerate(new_query_API['project_ID']):
        try:
            idx_saved_query = saved_query['project_ID'].index(id)
        except Exception as e:
            print(e)
            continue

        if new_query_API['project_status'][idx] != saved_query['project_status'][idx_saved_query]:
            status_change = True
            list_status_change_project.append(id)

    return (status_change, list_status_change_project)

def send_notification(tp_mod, message, item, data):

    message = f'''
    Nova alteração identificada: {message}
    Item modificado: {item}
    '''
    print(message)

def verify_modifications(new_query_API, saved_query):

    map_verifications = {
    'new_project':{'func':verify_new_project, 'message':'Novo Projeto Adicionado'}, 
    'delete_project':{'func':verify_delete_project, 'message':'Projeto deletado'},
    'status_change':{'func':verify_status_change_project, 'message':'Status do projeto alterado'}
    }

    for key, value in map_verifications.items():
        result_verification = value['func'](new_query_API, saved_query)
        if result_verification[0]:
            send_notification(key, value['message'], result_verification[1], new_query_API)
            save_new_json(new_query_API)

if __name__ == '__main__':

    data = get_data_Notion_API()
    new_query_API = transform_API_data(data)
    saved_query = load_save_json()
    verify_modifications(new_query_API, saved_query)