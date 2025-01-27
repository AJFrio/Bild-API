import os
import unittest
from unittest.mock import patch, MagicMock
from bild import Bild
import dotenv

dotenv.load_dotenv()

class TestBild(unittest.TestCase):

    @patch('bild.requests.get')
    def test_get_all_users(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        expected_data = {
            "data": [
                {
                    "id": "1",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "role": "admin",
                    "projects": []
                }
            ],
            "message": "Success"
        }
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        # Act
        bild = Bild(token='test_token')
        result = bild.get_all_users()

        # Assert
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with('https://api.getbild.com/users', headers={"Authorization": "Bearer test_token"})

    @patch('bild.requests.get')
    def test_get_all_projects(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        expected_data = {
            "data": [
                {
                    "id": "1",
                    "name": "Project A",
                    "users": [
                        {
                            "id": "1",
                            "name": "John Doe",
                            "accessType": "admin"
                        }
                    ],
                    "accessType": "admin"
                }
            ],
            "message": "Success"
        }
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        # Act
        bild = Bild(token='test_token')
        result = bild.get_all_projects()

        # Assert
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with('https://api.getbild.com/projects', headers={"Authorization": "Bearer test_token"})

    @patch('bild.requests.get')
    def test_get_all_files(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        expected_data = {
            "data": [
                {
                    "id": "1",
                    "name": "file1.txt",
                    "type": "text"
                }
            ],
            "message": "Success"
        }
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        # Act
        bild = Bild(token='test_token')
        bild.set_project('1')  # Set a project ID
        result = bild.get_all_files()

        # Assert
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with('https://api.getbild.com/projects/1/files', headers={"Authorization": "Bearer test_token"})

    # Add more test methods for other functions

if __name__ == '__main__':
    unittest.main() 