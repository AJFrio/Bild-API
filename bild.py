import os
import requests
import json
from requests import exceptions


class Bild:
    '''
    ## Bild API client

    Either set 'BILD_API_KEY' in environment variables or pass a token to the constructor: 
    token = <your_token>
    '''
    def __init__(self, token: str = 'env'):

        # Error messages
        self.auth_error = 'Authentication failed. Ensure you have a valid API key, that you have the correct permissions, and that you have passed it to the constructor.'
        self.path_error = 'Path not found. Bild has probably changed this endpoint.'
        self.token_error = 'No token found/provided. Please set BILD_API_KEY in environment variables or using the constructor argument, token = <your_token>'

        # Check for JWT token
        if token == 'env':
            self.token = os.getenv('BILD_API_KEY')
        else:
            self.token = token
        if self.token is None:
            raise Exception(self.token_error)
        else:   
            self.headers = {"Authorization": f"Bearer {self.token}"}
        
        self.baseurl = 'https://api.getbild.com'
        self.content_type = 'application/json;charset=UTF-8'
        self.branch = ''
        self.project = ''
        self.fileVersion = ''
        self.file = ''

    def set_branch(self, branch_id: str):
        self.branch = branch_id

    def set_project(self, project_id: str):
        self.project = project_id

    def set_file_version(self, file_version_id: str):
        self.fileVersion = file_version_id

    def set_file(self, file_id: str):
        self.file = file_id

    def check_response(self, response):
        '''
        Checks to see if the response has en error or is valid. Raises specific errors based on the response.
        '''
        if type(response) == str:
            raise Exception(response)
        else:
            return response.json()


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
        suffix = '/users'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()
    
    def add_users_to_bild(self, emails: list[str] = [], role: str = 'Member', projects: list[dict] = []):
        '''
        Add users to Bild. \n
        List of emails, each email as a string \n
        Role as a string (Member, Admin) Will be applied to all users in the list. Defaults to Member. \n
        List of projects, each project as a dictionary with the following keys: \n
        {
            "id": "string",
            "projectAccess": "string" (Editor, Viewer, Collaborator)
        } \n\n
        Example: \n
        {
            "emails": [
                "string@test.com",
                "string2@test.com"
                ...
            ],
            "role": "string",
            "projects": [
                {
                    "id": "string",
                    "projectAccess": "string" 
                }
                {
                    "id": "string",
                    "projectAccess": "string"
                }
                ...
            ]
        }

        '''
        if len(emails) == 0:
            raise Exception('No emails provided')
        suffix = '/users/add'
        data = {
            "emails": emails,
            "role": role,
            "projects": projects
        }
        response = requests.put(f"{self.baseurl}{suffix}", headers=self.headers, json=data)
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
        suffix = '/projects'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()
    
    def get_all_files(self, project_id = None):
        '''
        Get all files for a project as a JSON object:
        '''
        if project_id is None:
            project_id = self.project
        suffix = f'/projects/{project_id}/files'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()

    def get_all_users_in_project(self, project_id = None):
        '''
        Get all users in a project as a JSON object:
        '''
        if project_id is None:
            project_id = self.project
        suffix = f'/projects/{project_id}/users'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()

    def generate_stl(self, project_id = None, branch_id = None, file_id = None, file_version = None):
        '''
        Generate an STL file for a file.
        '''
        if project_id is None:
            project_id = self.project
        if branch_id is None:
            branch_id = self.branch
        if file_id is None:
            file_id = self.file
        if file_version is None:
            file_version = self.fileVersion
        suffix = f'/projects/{project_id}/branches/{branch_id}/files/{file_id}/universalFormat'
        data = {
            "fileVersion": file_version,
            "universalFileFormat": "stl"
        }
        response = requests.post(f"{self.baseurl}{suffix}", headers=self.headers, json=data, content_type=f'{self.content_type}: {data}')
        return response.json()

    def generate_step(self, project_id = None, branch_id = None, file_id = None, file_version = None):
        '''
        Generate a STEP file for a file.
        '''
        if project_id is None:
            project_id = self.project
        if branch_id is None:
            branch_id = self.branch
        if file_id is None:
            file_id = self.file
        if file_version is None:
            file_version = self.fileVersion
        suffix = f'/projects/{project_id}/branches/{branch_id}/files/{file_id}/universalFormat'
        data = {
            "fileVersion": file_version,
            "universalFileFormat": "step"
        }
        response = requests.post(f"{self.baseurl}{suffix}", headers=self.headers, json=data, content_type=f'{self.content_type}: {data}')
        return response.json()
    
    def get_all_metadata_fields(self):
        '''
        Get all metadata fields as a JSON object:
        '''
        suffix = '/metadataFields'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()
    
    def get_metadata_from_file(self, project_id = None, branch_id = None, file_id = None):
        '''
        Get metadata from a file as a JSON object:
        '''
        if project_id is None:
            project_id = self.project
        if branch_id is None:
            branch_id = self.branch
        if file_id is None:
            file_id = self.file
        suffix = f'/projects/{project_id}/branches/{branch_id}/files/{file_id}/metadata'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()
    
    def get_latest_file_version(self, project_id = None, branch_id = None, file_id = None):
        '''
        Get the latest file version as a JSON object:
        '''
        if project_id is None:
            project_id = self.project
        if branch_id is None:
            branch_id = self.branch
        if file_id is None:
            file_id = self.file
        suffix = f'/projects/{project_id}/branches/{branch_id}/files/{file_id}/latestFileVersion'
        response = requests.get(f"{self.baseurl}{suffix}", headers=self.headers)
        return response.json()

