import unittest
from unittest.mock import patch
from vulnerabilityManagement import upload_file, create_tag, create_zip_folder
from secret_functions import generate_random_password
import nc_py_api
from datetime import datetime, timedelta
import os
import pyzipper
import shutil


# Create a Nextcloud instance
def create_nextcloud_instance():
    return nc_py_api.Nextcloud(
        nextcloud_url="***",
        nc_auth_user="***",
        nc_auth_pass="***",
    )

class TestYourFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a test folder with a test.txt file
        test_folder = "Test"
        test_file_path = os.path.join(test_folder, "test.txt")

        # Create the text for the test.txt file
        os.makedirs(test_folder, exist_ok=True)
        with open(test_file_path, "w") as test_file:
            test_file.write("This is a test file.")

        # Create Test@test.uni-heidelberg.de.zip file with the test.txt file 
        test_zip_file_path = "Test@test.uni-heidelberg.de.zip"
        with pyzipper.AESZipFile(test_zip_file_path, "w", compression=pyzipper.ZIP_DEFLATED) as zip_file:
            zip_file.write(test_file_path)

    @classmethod
    # Clean up: delete folders and files
    def tearDownClass(cls):
        test_folder = "Test"
        test_folder_zip = "Test.zip"
        correct_enzippt_folder = "correct_unzipped"
        wrong_enzippt_folder = "wrong_unzipped"
        test_zip_file_path = "Test@test.uni-heidelberg.de.zip"

        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
            
        if os.path.exists(test_folder_zip):
            os.remove(test_folder_zip)

        if os.path.exists(correct_enzippt_folder):
            shutil.rmtree(correct_enzippt_folder)

        if os.path.exists(wrong_enzippt_folder):
            shutil.rmtree(wrong_enzippt_folder)

        if os.path.exists(test_zip_file_path):
            os.remove(test_zip_file_path)

    # Test if the function generates different passwords
    def test_upload_file(self):
        nc = create_nextcloud_instance()
        nextcloud_file_name = "Test@test.uni-heidelberg.de.zip"
        
        # Upload the test file to Nextcloud
        upload_file(nc, nextcloud_file_name, nextcloud_file_name)

        # Verify if the file was uploaded successfully
        files_api = nc.files
        all_files = files_api.listdir(depth=2, exclude_self=False)
        file_exists = any(file.name == nextcloud_file_name for file in all_files)
        self.assertEqual(file_exists, True)

        # Delete the uploaded file
        files_api.delete(files_api.by_path(nextcloud_file_name))

        # Verify if the file was deleted successfully
        all_files = files_api.listdir(depth=2, exclude_self=False)
        file_exists = any(file.name == nextcloud_file_name for file in all_files)
        self.assertEqual(file_exists, False)

    def test_create_tag(self):
        # Create a Nextcloud instance
        nc = create_nextcloud_instance()
        tag_name = "Greenbone Report 20-days"

        # Create a tag 
        create_tag(nc, tag_name)

        # Verify if the tag was created successfully
        tags = nc.files.list_tags()
        result = any(tag_name in tag.display_name for tag in tags)
        self.assertEqual(result, True)

    def test_create_zip_folder(self):
        file_name = "Test"
        file_name_zip ="Test.zip"

        # Create a zip folder and verify its existence
        create_zip_folder(file_name, file_name_zip,"CORRECTPASSWORD")
        self.assertTrue(os.path.isfile(file_name_zip))

    def test_unzip_zip_folder_correctPassword(self):
        file_name_zip = "Test.zip"
        password = "CORRECTPASSWORD"
        output_folder = "correct_unzipped"

        # Unzip the folder with the correct password 
        with pyzipper.AESZipFile(file_name_zip, "r") as zip_file:
            zip_file.pwd = password.encode()
            zip_file.extractall(output_folder)

        # Verify the extracted file and check if the test.txt file is in it
        extracted_files = os.listdir(output_folder)
        expected_file_name = 'test.txt'
        self.assertIn(expected_file_name, extracted_files)

    def test_unzip_zip_folder_wrongPassword(self):
        file_name_zip = "Test.zip"
        password = "WRONGPASSWORD" 
        output_folder = "wrong_unzipped"

        # Attempt to unzip the folder with the wrong password and expect a RuntimeError
        with self.assertRaises(RuntimeError) as context:
            with pyzipper.AESZipFile(file_name_zip, "r") as zip_file:
                zip_file.pwd = password.encode()
                zip_file.extractall(output_folder)

    def test_generate_random_password(self):
        password_1 = generate_random_password()
        password_2 = generate_random_password()
        self.assertNotEqual(password_1, password_2)

if __name__ == '__main__':
    unittest.main()
