import os
import requests
import json

class Bild:
    '''
    ## Bild API client

    Either set 'BILD_API_KEY' in environment variables or pass a token to the constructor: 
    token = <your_token>
    '''
    def __init__(self, token='env'):
        if token == 'env':
            self.token = os.getenv('BILD_API_KEY')
        else:
            self.token = token
        self.baseurl = 'https://sandbox-api.getbild.com'
        self.branch = ''
        self.project = ''
        self.file = ''


    def get_all_users(self):
        '''
        Get all users as a JSON object:
        {
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "email": "string",
                    "role": "string",
                    "projects": [
                        {
                            "id": "string",
                            "name": "string",
                            "accessType": "string"
                        }
                    ]
                }
            ],
            "message": "string"
        }
        '''
        response = requests.get(f"{self.baseurl}/users", headers={"Authorization": f"Bearer {self.token}"})
        return response.json()

    def get_all_projects(self):
        '''
        Get all projects as a JSON object:
        {
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "users": [
                        {
                            "id": "string",
                            "name": "string",
                            "accessType": "string"
                        }
                    ],
                    "accessType": "string"
                }
            ],
            "message": "string"
        }
        '''
        response = requests.get(f"{self.baseurl}/projects", headers={"Authorization": f"Bearer {self.token}"})
        return response.json()
    
    def get_all_files(self, project_id = None):
        if project_id is None:
            project_id = self.project
        response = requests.get(f"{self.baseurl}/projects/{project_id}/files", headers={"Authorization": f"Bearer {self.token}"})
        return response.json()
    
    def set_branch(self, branch_id: str):
        self.branch = branch_id

    def set_project(self, project_id: str):
        self.project = project_id

    def set_file(self, file_id: str):
        self.file = file_id

b = Bild()
