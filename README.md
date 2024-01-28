# Vulnerability Management System

## Overview
The Vulnerability Management System is a Python program designed to contact individuals responsible for IP addresses affected by vulnerabilities via email. Communication takes place via the Nextcloud platform, an onetimesecret service, and the sending of emails.

## Installation
1. Clone the repository: `git clone https://github.com/bwInfoSec/schwachstellenmgmt.git`
2. Navigate to the project directory: `cd schwachstellenmgmt`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Install the Python package: `pip install .`
5. Get more information about the system: `schwachstellenmgmt -h`
6. Start the script: `schwachstellenmgmt`

## User Input
The user has to enter some information so that the script can start:

1.  pdf-folder:
    - Path to the single_hosts folder of the Greenbone report.
    - This folder contains individual PDFs for each affected IP address.
        - The PDFs are named as follows: uni_heidelberg_Medium_[IP address].pdf

3.  json-file:
    - Path to the IP_Email JSON-file.
    - This JSON file contains mappings of IP addresses to email addresses.
    - The file have to be in the following structure: 
  
    `{
    
           "IP": "email",
    
           "IP": "email",
    
           "IP": "email",
    
           "IP": "email"
    
    }`
  
5.  credentials-path:
    - Path to a credentials.txt file.
    - This file contains all credentials needed for the script to run.
    - It's also possible to fill in the default credentials.txt file under the following path: "schwachstellenmgmt\templates\credentials.txt"
    - The script need following credentials: 
      nextcloud_url=
      nc_auth_user=
      nc_auth_pass=
      SMTP_domain=
      SMTP_port=
      SMTP_username=
      SMTP_password=
      SMTP_email=
      otp_domain=

6.  expiration-days:
        - Number of days until the link to the file in the Nextcloud should expire.
        - If nothing is entered then the default value ( = 14 days) will be selected.

7.  deletion-days:
        - Number of days until the files should be completely deleted from Nextcloud.
        - If nothing is entered then the default value ( = 14 days) will be selected.
    
8.  link_passwordzip_emailtext:
        - Path to a .txt file containing content for the email, which includes the link to Nextcloud and a one-time secret link for the password of the ZIP file.
        - The email content can be customized using placeholders like {nextcloud_file_url}, {zip_password_link}, and {expiration_date}.
        - If nothing is entered then the default value ("schwachstellenmgmt\templates\link_passwordZIP_emailText.txt") will be selected.

9.  passwordnextcloud_emailtext:
        - Path to a .txt file containing content for the email, which includes the one-time link for the password to Nextcloud.
        - The email content can be customized using the placeholder {nextcloud_password_link}.
        - If nothing is entered then the default value ("schwachstellenmgmt\templates\passwordNextcloud_emailText.txt") will be selected.

## Tests
To run the pytests, the user has to start a new Nextcloud instance so that the tests can also be run without the production system:
1.  The user needs the running program "Docker Desktop".
2.  Setup the Nextcloud instance: `docker-compose up -d`
3.  Start the pytests: `pytest`

## Content of the script: 
1.  The individual PDF files from the report are sorted by e-mail address and packed into a ZIP file
    - Include the json file with mapping IP to email and compare the IP addresses with the names of the PDF files (uni_heidelberg_Medium_[IP address].pdf) 
    - All PDFs grouped according to the email addresses are stored in a common folder ([email address])
    
2.  Login to Nextcloud 
3.  Create a tag:
    - The files on the Nextcloud will be deleted after x days
    - A tag with the name "Greenbone Report x-days" will be created for this purpose
    - After https://apps.nextcloud.com/apps/files_retention all files with the tag will be deleted after x days

    IMPORTANT: 
    A tag with the corresponding name is created so that the user can individually determine how long the files are available. To enable Nextcloud to make the corresponding settings for the tags, the administrator of the Nextcloud account must write another script in the background and integrate it. This is still outstanding! Until then, this feature will not be used.
    
4. ZIP files ([e-mail address].zip) are created from the folder from step 1
    - The ZIP file is protected with a password
    - The password for the ZIP file is provided via an one-time secret link

5. ZIP files are uploaded
    - The uploaded files are marked with the created tag
    - A link is created to the uploaded file 
    - The link is only valid for x days
    - Nextcloud access is also protected with a password
    - The password for the Nextcloud access is provided via an one-time secret link

6.  Two different emails are sent to one recipient
    - First contains the link to the file in the Nextcloud + one-time secret link to the password for the ZIP file
    - Second contains a one-time secret link to the password for the Nextcloud
