# apache-automation
Simple script written in Python/Bash to automate the setup process for an Apache web server for RHEL distros. 

This is a school project, not intended to for professional/enterprise use.

Full credit goes to AJ at html5up.net for the CSS templates being used.

# Details
This automation script will automate the setup of: 
- apache httpd install
- writing VirtualHosts to /etc/httpd/conf/httpd.conf
- TLS/SSL setup with mod_ssl
- index.html setup with 3 HTML/CSS templates to choose from (business, blog, portfolio)

# Requirements
- RHEL version 8.x or higher (must support dnf package manager)
- Python 3.x
- User with sudo permissions

# Download and run steps
To download the necessary files, either download as zip or use the git clone command. 
```
git clone https://github.com/bytefactorX/apache-automation.git
```

Once files are downloaded, begin the automation script by running:
```
./main.py
```
Sudo password will be required, and some system checks will be completed. Make sure to follow the instructions as needed for a successful setup.
