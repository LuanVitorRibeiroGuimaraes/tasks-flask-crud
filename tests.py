import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = [] #guarda os id's (basicamente uma lista de id's)

def test_create_task():
    new_task_data = {
        'title': 'nova tarefa',
        'description': 'descrição da tarefa'
    }
    response = requests.post(f'{BASE_URL}/tasks', json = new_task_data)

    assert response.status_code == 200
    response_json = response.json() #pegando os dados em json
    assert 'message' in response_json
    assert 'id' in response_json
    tasks.append(response_json['id'])

def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    response_json = response.json() #pegando os dados em json
    assert 'tasks' in response_json
    assert 'total_tasks' in response_json

def test_get_task():
    if tasks:
        task_id = tasks[0] #primeira atividade
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            'completed': False,
            'description': 'Nova descrição',
            'title': 'Título atualizado'
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json = payload)
        assert response.status_code == 200
        response_json = response.json()
        assert 'message' in response_json

        #nova requisição a tarefa específica
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json() #converte o json em dict python
        print(response_json.keys())
        assert response_json['title'] == payload['title']
        assert response_json['description'] == payload['description']
        assert response_json['completed'] == payload['completed']
    
def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200

        #nova requisição a tarefa específica
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404