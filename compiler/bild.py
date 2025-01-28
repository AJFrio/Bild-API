
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

    def get_all_users_in_bild_account(self):
        '''
        This endpoint returns the list of all user accounts in your Bild account, along with their IDs, names, emails, roles, and the projects they have access to.
        '''

        suffix = 'users'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_projects_in_bild_account(self):
        '''
        This endpoint returns all projects that the user has access to. If the user is an admin or has access to all projects in your Bild account, it returns them all. Each item contains the project's ID, name, users who are part of the project along with their IDs, names, and access types, as well as the default branch of the project.
        '''

        suffix = 'projects'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_users_in_project(self, projectID: str):
        '''
        This endpoint returns all users who are part of the project. Each item contains the user's ID, name, email, and access type.
        '''

        suffix = 'projects/{projectID}/users'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_branches_of_project(self, projectID: str):
        '''
        This endpoint returns all branches of the given project, including their IDs and names.
        '''

        suffix = 'projects/{projectID}/branches'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_commits_of_project(self, projectID: str):
        '''
        This endpoint returns all commits of the project, providing a history of all file update activities across branches with pagination. For the first page, provide the pageSize parameter in the query parameters. For subsequent pages, provide the lastEvaluatedKey received as a response from the previous call.
        '''

        suffix = 'projects/{projectID}/commits'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_commits_of_branch(self, projectID: str, branchID: str):
        '''
        This endpoint returns all commits of the branch, providing a history of all file update activities within the branch with pagination. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/commits'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_commit_details(self, projectID: str, branchID: str, commitID: str):
        '''
        This endpoint returns details of the commit for the given commitID, along with all the files involved in that commit. Each file will include its ID, name, part number, and revision number at the time of the commit.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/commits/{commitID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_released_files_after_time(self):
        '''
        This endpoint returns all files that were released after the given time. If a file is released multiple times, it will only return the latest instance for that file. The time is expected in Unix timestamp (Epoch), including milliseconds.
        '''

        suffix = 'files/released'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_files_default_branch(self, projectID: str):
        '''
        This endpoint returns all the latest versions of files from the project's default branch. Each entry will include fields such as name, id, type, path, latestVersionID etc. Response can be a flat list of files or a file-folder tree structure. By default, it'll be a file-folder tree structure.
        '''

        suffix = 'projects/{projectID}/files'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_files_for_branch(self, projectID: str, branchID: str):
        '''
        This endpoint returns all the latest versions of files for the given branch ID. Each entry will include fields such as name, fileID, path, and latestVersionID. Response can be queried as a flat list of files or a file-folder tree structure. By default, it'll be a file-folder tree structure.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_versions_of_file(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint returns all file versions for the given fileID. Each version entry will contain basic file details such as name, id, and path, along with metadata. Please note that, metadata will be just "File Properties" data. For more detailed metadata, use /projects/{projectID}/branches/{branchID}/files/{fileID}/metadata and other metadata APIs.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/versions'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_latest_version_of_file(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint retrieves details of the latest file version.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/latest'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_latest_released_version_of_file(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint retrieves details of the latest released file.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/released'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_file_version(self, projectID: str, branchID: str, fileID: str, fileVersionID: str):
        '''
        This endpoint retrieves file version details for the given fileVersionID.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/versions/{fileVersionID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_public_shared_files_links_bild_account(self):
        '''
        This endpoint returns all public shared file links in your Bild account in paginated format. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. The shared link contains details such as name, type, and the public URL.
        '''

        suffix = 'sharedLinks'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_public_shared_files_links(self, projectID: str):
        '''
        This endpoint returns all public shared file links in your project in paginated format. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. The shared link contains details such as name, type, and the public URL.
        '''

        suffix = 'projects/{projectID}/sharedLinks'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_public_shared_files_links_in_branch(self, projectID: str, branchID: str):
        '''
        This endpoint returns all public shared file links in your branch in paginated format. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. The shared link contains details such as name, type, and the public URL.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/sharedLinks'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_custom_metadata_fields(self):
        '''
        This endpoint returns all metadata fields, including Bild's default fields and custom fields created by users.
        '''

        suffix = 'metadataFields'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_complete_metadata_for_file(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint returns metadata details for the file version associated with the given fileID. Metadata includes all fields and values across all available configs/profiles. By default, users will get metadata for the latest versions of the file.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/metadata'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_complete_metadata_for_file_version(self, projectID: str, branchID: str, fileID: str, fileVersionID: str):
        '''
        This endpoint returns metadata details for the fileVersionID. Metadata includes all fields and values across all available configs/profiles.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/versions/{fileVersionID}/metadata'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_feedback_items_in_project(self, projectID: str):
        '''
        This endpoint returns all feedback items in the project with pagination. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. Each feedback item contains details such as title, description, status, due date, tags, assignees, comments, attachments, etc.
        '''

        suffix = 'projects/{projectID}/feedbackItems'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_feedback_items_for_file(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint returns all feedback items for a file. Each feedback item contains details such as title, description, status, due date, tags, assignees, comments, attachments, etc.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/feedbackItems'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_feedback_item_details_by_id(self, projectID: str):
        '''
        This endpoint returns feedback item details for the given feedback item ID. Each feedback item contains details such as title, description, status, due date, tags, assignees, comments, attachments, etc.
        '''

        suffix = 'projects/{projectID}/feedbackItems/{feedbackItemID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_packages_from_bild_account(self):
        '''
        This endpoint returns all packages in your Bild account. The results are paginated. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. Each package contains basic details such as name, creator name, created date, number of files, etc.
        '''

        suffix = 'packages'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_packages_in_project(self, projectID: str):
        '''
        This endpoint returns all packages in the project in paginated format. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. Each package contains basic details such as name, creator name, created date, number of files, etc.
        '''

        suffix = 'projects/{projectID}/packages'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_detailed_package_info_by_id(self, projectID: str):
        '''
        This endpoint retrieves details of all package information, including all files in the package. Each package contains details such as name, creator name, created date, a list of files, and a download URL for the package.
        '''

        suffix = 'projects/{projectID}/packages/{packageID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_ecos_in_bild_account(self):
        '''
        This endpoint returns all Engineering Change Orders (ECOs) in your company's Bild account. The API supports paginated queries of ECOs. Users can pass pageSize and lastEvaluatedKey. PageSize determines the number of records per page, while lastEvaluatedKey serves as an offset key similar to database pagination. In the first API call, you'll receive the lastEvaluatedKey, which can be used in the next API call.
        '''

        suffix = 'ecos'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_ecos_in_project(self, projectID: str):
        '''
        This endpoint returns all Engineering Change Orders (ECOs) in the given project. Similar to the above, the API supports pagination with pageSize and lastEvaluatedKey, along with filtering the responses based on the status of the ECO.
        '''

        suffix = 'projects/{projectID}/ecos'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_ecos_of_branch_project(self, projectID: str, branchID: str):
        '''
        This endpoint returns all Engineering Change Orders (ECOs) in the given branch of the project. Similar to the above, the API supports pagination with pageSize and lastEvaluatedKey, along with filtering the responses based on the status of the ECO.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/ecos'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_ecos_of_file_in_branch(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint returns all Engineering Change Orders (ECOs) in the given file of the branch in the project. Similar to the above, the API supports pagination with pageSize and lastEvaluatedKey, along with filtering the responses based on the status of the ECO.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/ecos'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_details_of_eco(self, projectID: str, branchID: str, fileID: str, ecoID: str):
        '''
        This endpoint returns details of an Engineering Change Order (ECO), along with all the file versions involved in that ECO. It also provides the list of all approvals that are part of that ECO.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/ecos/{ecoID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_all_part_files_and_sub_assemblies(self, projectID: str, branchID: str, fileID: str):
        '''
        This endpoint returns a list of all part files and sub-assemblies of an assembly file. It provides the full closure of the file, i.e., the list of all part files and sub-assemblies of an assembly file. These closures are configuration-specific. This endpoint is useful for obtaining the full closure of the file when the user intends to release/cancel the ECO for assembly file along with all its part files and sub-assemblies.
        '''

        suffix = 'projects/{projectID}/branches/{branchID}/files/{fileID}/closure'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_approval_requests_bild_account(self):
        '''
        This endpoint returns all approval requests in your Bild account. By default, it returns the active approvals, i.e. Approvals those are PENDING in status. Pagination is supported using pageSize and lastEvaluatedKey, similar to the above APIs.
        '''

        suffix = 'approvals'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_approval_requests_in_project(self, projectID: str):
        '''
        This endpoint returns all approval requests in the project in paginated format. By default, it returns the active approvals, i.e. Approvals those are PENDING in status. For the first page, simply pass the pageSize in the query parameters. For subsequent pages, pass the lastEvaluatedKey received as a response from the previous call. Each approval request contains basic details such as name, creator name, created date, file name, etc., along with the list of active reviewers.
        '''

        suffix = 'projects/{projectID}/approvals'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    

    def get_details_of_approval_request(self, projectID: str, approvalID: str):
        '''
        This endpoint returns details of an approval request along with active reviewers.
        '''

        suffix = 'projects/{projectID}/approvals/{approvalID}'
        url = f'self.baseurl/{suffix}'
        response = requests.request('GET', url, headers=self.headers)
        return self.check_response(response)
    