# Bild API Client

## Introduction
The `Bild` class is a client for interacting with the Bild API. It allows users to manage projects, users, and files within the Bild platform. The client can be used to retrieve information, add users, and generate STL files from project files.

## Installation
1. Clone the repository.
2. Ensure you have Python installed (version 3.6 or higher).
3. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To use the `Bild` class, you need to instantiate it with a valid API token. You can either set the `BILD_API_KEY` environment variable or pass the token directly to the constructor.

Example:
```python
from bild import Bild

# Using environment variable
client = Bild()

# Passing token directly
client = Bild(token='your_api_token')
```

## Configuration
Set the `BILD_API_KEY` in your environment variables or pass it directly to the `Bild` class constructor.

## Methods
- `set_branch(branch_id)`: Set the branch ID for operations.
- `set_project(project_id)`: Set the project ID for operations.
- `set_file(file_id)`: Set the file ID for operations.
- `get_all_users()`: Retrieve all users.
- `add_users_to_bild(emails, role, projects)`: Add users to Bild with specified roles and projects.
- `get_all_projects()`: Retrieve all projects.
- `get_all_files(project_id)`: Retrieve all files for a specified project.
- `get_all_users_in_project(project_id)`: Retrieve all users in a specified project.
- `generate_stl(project_id, branch_id, file_id)`: Generate an STL file for a specified file.

## Error Handling
The client raises exceptions for authentication errors, missing tokens, and path errors. Ensure you handle these exceptions in your application.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. 