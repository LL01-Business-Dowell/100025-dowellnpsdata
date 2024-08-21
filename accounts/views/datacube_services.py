import requests

class DatacubeServices:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://datacube.uxlivinglab.online/db_api'

    def data_insertion(self, database_name, collection_name, data):
        url = f'{self.base_url}/crud/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'coll_name': collection_name,
            'operation': 'insert',
            'data': data,
            'payment': False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error inserting data', 'error': str(e)}

    def data_retrieval(self, database_name, collection_name, filters, limit, offset):
        url = f'{self.base_url}/get_data/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'coll_name': collection_name,
            'operation': 'fetch',
            'filters': filters,
            'limit': limit,
            'offset': offset,
            'payment': False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error retrieving data', 'error': str(e)}

    def data_update(self, database_name, collection_name, query, update_data):
        url = f'{self.base_url}/crud/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'coll_name': collection_name,
            'operation': 'update',
            'query': query,
            'update_data': update_data,
            'payment': False
        }
        try:
            response = requests.put(url, json=payload)
            response.raise_for_status()
            return {'success': True, 'message': 'Data updated successfully', 'response': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error updating data', 'error': str(e)}

    def create_collection(self, database_name, collection_name):
        url = f'{self.base_url}/add_collection/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'coll_names': collection_name,
            'num_collections': 1
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error creating collection', 'error': str(e)}

    def collection_retrieval(self, database_name):
        url = f'{self.base_url}/collections/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'payment': False
        }
        try:
            response = requests.get(url, json=payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error retrieving collections', 'error': str(e)}

    def data_delete(self, database_name, collection_name, query):
        url = f'{self.base_url}/crud/'
        payload = {
            'api_key': self.api_key,
            'db_name': database_name,
            'coll_name': collection_name,
            'operation': 'delete',
            'query': query
        }
        try:
            response = requests.delete(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': 'Error deleting data', 'error': str(e)}

