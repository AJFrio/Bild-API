import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

with open('compiler/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    file.close()

def chat(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": 'You are used to help come up with straight forward  and easy to remember function names for python functions. You will be given a name and you have to come up with a simple snake case name. only respond with the name of the function. no other text.'},
                  {"role": "user", "content": prompt}
                  ] 
    )
    return response.choices[0].message.content

def get_template(info: list) -> str:
    name = chat(info['name'])
    parameters = ''
    if 'projectID' in info['url']:
        parameters += f', projectID: str = self.project'
    if 'branchID' in info['url']:
        parameters += f', branchID: str = self.branch'
    if 'commitID' in info['url']:
        parameters += f', commitID: str = self.commit'
    if 'fileID' in info['url']:
        parameters += f', fileID: str = self.file'
    if 'fileVersionID' in info['url']:
        parameters += f', fileVersionID: str = self.fileVersion'
    if 'ecoID' in info['url']:
        parameters += f', ecoID: str = self.eco'
    if 'approvalID' in info['url']:
        parameters += f', approvalID: str = self.approval'
    template = f"""
    def {name}(self{parameters}):
        ###
        {info['description']}
        ###

        suffix = f#{str(info['url']).split('getbild.com/')[1]}#
        url = f#self.baseurl/<suffix>#
        response = requests.request(#{info['request_type']}#, url, headers=self.headers)
        return self.check_response(response)
    """
    return template

init_class = """
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
        self.commit = ''
        self.eco = ''
        self.approval = ''

    def set_branch(self, branch_id: str):
        self.branch = branch_id

    def set_project(self, project_id: str):
        self.project = project_id

    def set_file_version(self, file_version_id: str):
        self.fileVersion = file_version_id

    def set_file(self, file_id: str):
        self.file = file_id
    
    def set_commit(self, commit_id: str):
        self.commit = commit_id

    def set_eco(self, eco_id: str):
        self.eco = eco_id

    def set_approval(self, approval_id: str):
        self.approval = approval_id

    def check_response(self, response):
        '''
        Checks to see if the response has en error or is valid. Raises specific errors based on the response.
        '''
        if type(response) == str:
            raise Exception(response)
        else:
            return response.json()
"""

functions = []
for item in data['get_urls']:
    functions.append(str(get_template(item)).replace('#', "'").replace('<', '{').replace('>', '}'))

with open('compiler/bild.py', 'w', encoding='utf-8') as file:
    file.write(init_class + '\n'.join(functions))
    file.close()


