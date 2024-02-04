# Vulnerability Management System

## Overview
The Vulnerability Management System is a Python program designed to contact individuals responsible for IP addresses affected by vulnerabilities via email. Communication takes place via the Nextcloud platform, an one-time secret service, and the sending of emails.

## Installation
1. Clone the repository: `git clone https://github.com/bwInfoSec/schwachstellenmgmt.git`
2. Navigate to the project directory: `cd schwachstellenmgmt`
3. (Optional: A virtual environment can be created with Python: `python -m venv env` )
4. Install the required dependencies: `pip install -r requirements.txt`
5. Install the Python package: `pip install .`
6. Get more information about the system: `schwachstellenmgmt -h`
7. Start the script: `schwachstellenmgmt`

## User Input
The user has to enter some information to start the script:

1.  pdf-folder:
    - Path to the single_hosts folder of the Greenbone report.
    - This folder contains individual PDFs for each affected IP address.
        - The PDFs are named as follows: `[...]_[IP address].pdf`

2.  json-file:
    - Path to the IP_Email JSON file.
    - This JSON file contains mappings of IP addresses to email addresses.
    - The file has to be in the following structure: 
  
```json
{
    "IP": "email",
    "IP": "email",
    "IP": "email",
    "IP": "email"
}
```
  
3.  credentials-path:
    - Path to a credentials.txt file.
    - This file contains all credentials needed for the script to run.
    - It's also possible to fill in the default credentials.txt file under the following path: `schwachstellenmgmt\templates\credentials.txt`
    - The script needs following credentials: 
```plaintext
nextcloud_url=
nc_auth_user=
nc_auth_pass=
SMTP_domain=
SMTP_port=
SMTP_username=
SMTP_password=
SMTP_email=
ots_domain=
```

4.  expiration-days:
    - Number of days until the link to the file in the Nextcloud will expire.
    - If no input is made, the default value `14 days` is set. 

5.  deletion-days:
    - Number of days until the files will be completely deleted from Nextcloud.
    - If no input is made, the default value `14 days` is set. 
    
6.  link_passwordzip_emailtext:
    - Path to a .txt file containing content for the email, which includes the link to Nextcloud and a one-time link for the password of the ZIP file.
    - The email content can be customized using placeholders like `{nextcloud_file_url}`, `{zip_password_link}`, and `{expiration_date}`.
    - If no input is made, the default value `schwachstellenmgmt\templates\link_passwordZIP_emailText.txt` is set.

7.  passwordnextcloud_emailtext:
    - Path to a .txt file containing content for the email, which includes the one-time link for the password to Nextcloud.
    - The email content can be customized using the placeholder `{nextcloud_password_link}`.
    - If no input is made, the default value `schwachstellenmgmt\templates\passwordNextcloud_emailText.txt` is set.

## Tests
To run the pytests, the user has to start a new Nextcloud instance so that the tests can also be run without the production system:
1.  The user needs the running program "Docker Desktop".
2.  Setup the Nextcloud instance: `docker-compose up -d`
3.  Wait a few seconds until the setup of the Nextcloud container is complete.
4.  Start the pytests: `pytest`

## Content of the script: 
1.  The individual PDF files of the report are sorted by email addresses and packed into a ZIP file
    - This step contains the JSON file with the assignment of IP to email and compares the IP addresses with the names of the PDF files (uni_heidelberg_Medium_[IP address].pdf).
    -  All PDFs are grouped by email address and saved in a same folder ([email address]).
      
2.  Login to Nextcloud
   
3.  Create a tag:
    - The files on the Nextcloud will be deleted after x days
    - For this purpose, a tag with the name `Greenbone Report x-days` is created
    - According to `https://apps.nextcloud.com/apps/files_retention` all files with the tag will be deleted after x days

    `IMPORTANT: 
    The user can select the number of days after which the file is to be completely deleted at the start of the script. A tag with the corresponding name is created so that the user can individually determine how long the files are available. In order for Nextcloud to make the appropriate settings for the tags, the administrator of the Nextcloud account must write another script in the background and integrate it. This has not yet been done! Until then, this function will not be used.`
    
4.  ZIP files ([email address].zip) are created from the folder from step 1
    - The ZIP file is protected with a password
    - The password for the ZIP file is provided via a one-time link

5.  ZIP files are uploaded
    - The uploaded files are marked with the tag created
    - A link to the uploaded file is created 
    - The link will only be valid for x days
    - Nextcloud access is also protected with a password
    - The password for Nextcloud access is provided via a one-time link

6.  Two different emails are sent to one recipient
    - The first contains the link to the file in the Nextcloud + a one-time link to the password for the ZIP file
    - The second contains a one-time link to the password for the Nextcloud
