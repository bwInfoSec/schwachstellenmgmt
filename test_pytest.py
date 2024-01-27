import os
import shutil
import pytest
import pyzipper
from schwachstellenmgmt.vulnerability_management import upload_file, create_tag, create_zip_folder
from schwachstellenmgmt.secret_functions import generate_random_password
import nc_py_api

@pytest.fixture(scope="session", autouse=True)
def setup_before_tests():
    # Create a test folder with a test.txt file
    test_folder = "schwachstellenmgmt\\Test"
    test_file_path = os.path.join(test_folder, "test.txt")

    # Create the text for the test.txt file
    os.makedirs(test_folder, exist_ok=True)
    with open(test_file_path, "w") as test_file:
        test_file.write("This is a test file.")

    # Create Test@test.uni-heidelberg.de.zip file with the test.txt file 
    test_zip_file = "schwachstellenmgmt\\Test@test.uni-heidelberg.de.zip"
    with pyzipper.AESZipFile(test_zip_file, "w", compression=pyzipper.ZIP_DEFLATED) as zip_file:
        zip_file.write(test_file_path)

@pytest.fixture(scope="session")
def nc_instance():
    return nc_py_api.Nextcloud(
        nextcloud_url="http://localhost:8080",
        nc_auth_user="admin",
        nc_auth_pass="admin_password",
    )

def test_upload_file(nc_instance):

    test_zip_file = "Test@test.uni-heidelberg.de.zip"

    # Upload the test file to Nextcloud
    upload_file(nc_instance, test_zip_file, test_zip_file)

    # Verify if the file was uploaded successfully
    files_api = nc_instance.files
    all_files = files_api.listdir(depth=2, exclude_self=False)
    assert any(file.name == test_zip_file for file in all_files)

    # Delete the uploaded file
    files_api.delete(files_api.by_path(test_zip_file))

    # Verify if the file was deleted successfully
    all_files = files_api.listdir(depth=2, exclude_self=False)
    assert not any(file.name == test_zip_file for file in all_files)


def test_create_tag(nc_instance):
    tag_name = "Greenbone Report 20-days"
    create_tag(nc_instance, tag_name)

    # Verify if the tag was created successfully
    tags = nc_instance.files.list_tags()
    assert any(tag_name in tag.display_name for tag in tags)


def test_create_zip_folder():
    folder_name = "schwachstellenmgmt\\Test"
    folder_name_zip = "schwachstellenmgmt\\Test.zip"
    password = "CORRECTPASSWORD"
    

    # Create a zip folder and verify its existence
    create_zip_folder(folder_name, folder_name_zip, password)
    assert os.path.isfile(folder_name_zip)



def test_unzip_zip_folder_correctPassword():
    folder_name_zip = "schwachstellenmgmt\\Test.zip"
    password = "CORRECTPASSWORD"
    output_folder = "schwachstellenmgmt\\correct_unzipped"



    # Unzip the folder with the correct password
    with pyzipper.AESZipFile(folder_name_zip, "r") as zip_file:
        zip_file.pwd = password.encode()
        zip_file.extractall(output_folder)

    # Verify the extracted file and check if the test.txt file is in it
    extracted_files = os.listdir(output_folder)
    expected_file_name = 'test.txt'
    assert expected_file_name in extracted_files


def test_unzip_zip_folder_wrongPassword():
    folder_name_zip = "schwachstellenmgmt\\Test.zip"
    output_folder = "schwachstellenmgmt\\wrong_unzipped"
    password = "WRONGPASSWORD" 


    # Attempt to unzip the folder with the wrong password and expect a RuntimeError
    with pytest.raises(RuntimeError):
        with pyzipper.AESZipFile(folder_name_zip, "r") as zip_file:
            zip_file.pwd = password.encode()
            zip_file.extractall(output_folder)


def test_generate_random_password():
    password_1 = generate_random_password()
    password_2 = generate_random_password()
    assert password_1 != password_2

@pytest.fixture(scope="session", autouse=True)
def final_cleanup(request):
    test_folder = "schwachstellenmgmt\\Test"
    test_folder_zip = "schwachstellenmgmt\\Test.zip"
    correct_enzippt_folder = "schwachstellenmgmt\\correct_unzipped"
    wrong_enzippt_folder = "schwachstellenmgmt\\wrong_unzipped"
    test_zip_file = "schwachstellenmgmt\\Test@test.uni-heidelberg.de.zip"

    # Das Cleanup-Funktionsobjekt wird erstellt
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

    # Das Cleanup-Funktionsobjekt wird dem finalizer hinzugefügt
    request.addfinalizer(cleanup)
