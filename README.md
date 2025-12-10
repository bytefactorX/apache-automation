# apache-automation
Simple script written in Python/Bash to automate the setup process for an Apache web server for RHEL distros. 

This is a school project, not intended to for professional/enterprise use.

# Details
This automation script will automate the setup of: 
- apache httpd install
- writing VirtualHost's to /etc/httpd/conf/httpd.conf
- TLS/SSL setup with mod_ssl
- index.html setup with 3 HTML/CSS templates to choose from (business, blog, portfolio)

# Download and run steps
To download the necessary files, either download as zip or use the git clone command. 

Once files are downloaded, begin the automation script by running:
```
./main.py
```
Sudo password will be required, and some system checks will be completed. Make sure to follow the instructions as needed for a successful setup.
