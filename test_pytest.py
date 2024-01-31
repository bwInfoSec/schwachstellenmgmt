"""
test_pytest.py contains unit tests for the schwachstellenmgmt package. 

It includes tests for:
- Creating a tag in Nextcloud.
- Uploading a file to Nextcloud.
- Creating a zip folder.
- Unzipping a zip folder with correct and incorrect passwords.
- Generating a random password.

These tests utilize fixtures for setup and cleanup before and after testing.
"""

import os
import shutil
import pytest
import pyzipper
from schwachstellenmgmt.vulnerability_management import upload_file, create_tag, create_zip_folder
from schwachstellenmgmt.secret_functions import generate_random_password
import nc_py_api

@pytest.fixture(scope="session", autouse=True)
def setup_before_tests():
    """
    Fixture to set up necessary files and folders before running tests.
    
    Creates a test folder with a test.txt file.
    Creates a zip file containing the test.txt file.
    """
    test_folder = "schwachstellenmgmt/Test"
    test_folder = os.path.normpath(test_folder)

    test_file_path = os.path.join(test_folder, "test.txt")

    os.makedirs(test_folder, exist_ok=True)
    with open(test_file_path, "w") as test_file:
        test_file.write("This is a test file.")

    test_zip_file = "schwachstellenmgmt/Test@test.uni-heidelberg.de.zip"
    test_zip_file = os.path.normpath(test_zip_file)
    
    with pyzipper.AESZipFile(test_zip_file, "w", compression=pyzipper.ZIP_DEFLATED) as zip_file:
        zip_file.write(test_file_path)

@pytest.fixture(scope="session")
def nc_instance():
    """
    Fixture to provide a Nextcloud instance for testing.
    
    Returns:
        nc_py_api.Nextcloud: An instance of Nextcloud.
    """
    return nc_py_api.Nextcloud(
        nextcloud_url="http://localhost:8080",
        nc_auth_user="admin",
        nc_auth_pass="admin_password",
    )

def test_create_tag(nc_instance):
    """
    Test case for creating a tag in Nextcloud.

    Args:
        nc_instance (nc_py_api.Nextcloud): Instance of Nextcloud.
    """
    tag_name = "test_tag"
    create_tag(nc_instance, tag_name)

    tags = nc_instance.files.list_tags()
    assert any(tag_name in tag.display_name for tag in tags)

def test_upload_file(nc_instance):
    """
    Test case for uploading a file to Nextcloud.

    Args:
        nc_instance (nc_py_api.Nextcloud): Instance of Nextcloud.
    """
    test_zip_file = "Test@test.uni-heidelberg.de.zip"
    deletion_tag = "test_tag"

    upload_file(nc_instance, test_zip_file, test_zip_file, deletion_tag)

    files_api = nc_instance.files
    all_files = files_api.listdir(depth=2, exclude_self=False)
    assert any(file.name == test_zip_file for file in all_files)

    files_api.delete(files_api.by_path(test_zip_file))

    all_files = files_api.listdir(depth=2, exclude_self=False)
    assert not any(file.name == test_zip_file for file in all_files)


def test_create_zip_folder():
    """
    Test case for creating a zip folder.
    """
    folder_name = "schwachstellenmgmt/Test"
    folder_name = os.path.normpath(folder_name)

    folder_name_zip = "schwachstellenmgmt/Test.zip"
    folder_name_zip = os.path.normpath(folder_name_zip)
    password = "CORRECTPASSWORD"
    
    create_zip_folder(folder_name, folder_name_zip, password)
    assert os.path.isfile(folder_name_zip)

def test_unzip_zip_folder_correctPassword():
    """
    Test case for unzipping a zip folder with correct password.
    """
    folder_name_zip = "schwachstellenmgmt/Test.zip"
    folder_name_zip = os.path.normpath(folder_name_zip)

    output_folder = "schwachstellenmgmt/correct_unzipped"
    output_folder = os.path.normpath(output_folder)

    password = "CORRECTPASSWORD"

    with pyzipper.AESZipFile(folder_name_zip, "r") as zip_file:
        zip_file.pwd = password.encode()
        zip_file.extractall(output_folder)

    extracted_files = os.listdir(output_folder)
    expected_file_name = 'test.txt'
    assert expected_file_name in extracted_files


def test_unzip_zip_folder_wrongPassword():
    """
    Test case for attempting to unzip a zip folder with incorrect password.
    """
    folder_name_zip = "schwachstellenmgmt/Test.zip"
    folder_name_zip = os.path.normpath(folder_name_zip)

    output_folder = "schwachstellenmgmt/wrong_unzipped"
    output_folder = os.path.normpath(output_folder)

    password = "WRONGPASSWORD" 

    with pytest.raises(RuntimeError):
        with pyzipper.AESZipFile(folder_name_zip, "r") as zip_file:
            zip_file.pwd = password.encode()
            zip_file.extractall(output_folder)


def test_generate_random_password():
    """
    Test case for generating a random password.
    """
    password_1 = generate_random_password()
    password_2 = generate_random_password()
    assert password_1 != password_2

@pytest.fixture(scope="session", autouse=True)
def final_cleanup(request):
    """
    Fixture to perform cleanup after running tests.

    Removes created files and folders.
    """
    test_folder = "schwachstellenmgmt/Test"
    test_folder = os.path.normpath(test_folder)

    test_folder_zip = "schwachstellenmgmt/Test.zip"
    test_folder_zip = os.path.normpath(test_folder_zip)

    correct_enzippt_folder = "schwachstellenmgmt/correct_unzipped"
    correct_enzippt_folder = os.path.normpath(correct_enzippt_folder)

    wrong_enzippt_folder = "schwachstellenmgmt/wrong_unzipped"
    wrong_enzippt_folder = os.path.normpath(wrong_enzippt_folder)

    test_zip_file = "schwachstellenmgmt/Test@test.uni-heidelberg.de.zip"
    test_zip_file = os.path.normpath(test_zip_file)

    def cleanup():
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        if os.path.exists(test_folder_zip):
            os.remove(test_folder_zip)
        if os.path.exists(correct_enzippt_folder):
            shutil.rmtree(correct_enzippt_folder)
        if os.path.exists(wrong_enzippt_folder):
            shutil.rmtree(wrong_enzippt_folder)
        if os.path.exists(test_zip_file):
            os.remove(test_zip_file)

    request.addfinalizer(cleanup)
