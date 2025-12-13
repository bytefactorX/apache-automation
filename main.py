#!/usr/bin/env python3

# file to handle main automation logic
# including running bash script,
# and running the two conf file scripts

import subprocess
import re
import os

# script constants
HOME = os.path.expanduser("~")
INTERFACE = "ens160"
ROOT = "/var/www/html"
HTTP = 80
HTTPS = 443

# import other python scripts
from conf import update_http_conf, update_https_conf

# manual IP address will be required 
# to ensure best practices are being exercised
def chk_ip_addr():
    print("Checking default interface for IPv4 method...")
    # capture output to use after process completed
    ip_method = subprocess.run(f"nmcli con show {INTERFACE} | grep ipv4.method", capture_output=True, text=True, shell=True)

    if "auto" in ip_method.stdout:
        print("Please change IPv4 method to manual before proceeding.")
        # simple check to ensure user switches to manual IP
        # if they do not, code will still run, as this is just a warning
        # and not an error
        ip_prompt = input("Press Enter when changes have been made: ")
        if ip_prompt == "":
            print("Proceeding...")
    else:
        print("IPv4 method is set to manual. Proceeding...")


# handles the string parsing to create the web directory 
def get_web_dir():
    while True:
        mk_prompt = input("Enter the FQDN of your website here (example: www.mydomain.net): ")
        # remove whitespace throughout the input
        f_mk_prompt = mk_prompt.replace(" ", "")

        # valid characters for a website name
        valid_chrs = r'[A-Za-z0-9.-]'
        
        # all checks necessary to create valid website (avoid any user errors)
        if not re.match(valid_chrs, f_mk_prompt):
            print("Invalid website name. Please try again.")
        else:
            print("Valid website name. Script will continue as usual...")
            print(f_mk_prompt)
            break
    
    return f_mk_prompt


# make the dir, cp it to /var/www/html, and change owner
def mk_web_dir(f_mk_prompt):
    dir_path = os.path.join(HOME, f_mk_prompt) 
    
    if os.path.exists(dir_path):
        print("Directory already exists. Please go back and make a unique directory.")
        # run func again to make unique dir        
        get_web_dir()
    else:
        print("Creating directory in home...")
        subprocess.run(f"mkdir {HOME}/{f_mk_prompt}", shell=True)

    try:
        print("Sending directory to document root...")
        subprocess.run(["sudo", "cp", "-R", f"{HOME}/{f_mk_prompt}", f"{ROOT}/{f_mk_prompt}"], check=True)

        # change directory ownership to apache:apache
        subprocess.run(["sudo", "chown", "-R", "apache:apache", f"{ROOT}/{f_mk_prompt}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with subprocess: {e}")


# choose from the templates available
# and cp into the directory
def select_template(f_mk_prompt):
    temp_options = """
        Template options:
        no template    displays default apache page
        business       displays a basic business-style page
        blog           displays a basic blog-style page
        portfolio      displays a basic portfolio-style page    
    """
    temp_prompt = input("Pick which style to use:  ")
    
    # if no template, insert most basic index.html file 
    # for basic access
    match temp_prompt.lower():
        case 'no template':
            # do nothing
            print("No template selected. Continuing...")
        case 'business':
            print("Selecting business template...")
            # cp to home dir first
            subprocess.run(["cp", "-R", "templates/business", f"{HOME}/{f_mk_prompt}/business"])
            # then cp to doc root
            subprocess.run(["sudo", "cp", "-R", f"{HOME}/{f_mk_prompt}/business", f"{ROOT}/{f_mk_prompt}/business"])
            print("Business template successfully added.")
        case 'blog':
            print("Selecting blog template...")
            # cp to home dir first
            subprocess.run(["cp", "-R", "templates/blog", f"{HOME}/{f_mk_prompt}/blog"])
            # then cp to doc root
            subprocess.run(["sudo", "cp", "-R", f"{HOME}/{f_mk_prompt}/blog", f"{ROOT}/{f_mk_prompt}/blog"])
            print("Blog template successfully added.")
        case 'portfolio':
            print("Selecting portfolio template...")
            # cp to home dir first
            subprocess.run(["cp", "-R", "templates/portfolio", f"{HOME}/{f_mk_prompt}/portfolio"])
            # then cp to doc root
            subprocess.run(["sudo", "cp", "-R", f"{HOME}/{f_mk_prompt}/portfolio", f"{ROOT}/{f_mk_prompt}/portfolio"])
            print("Portfolio template successfully added.")
        case _:
            print("Please type a valid response.")


def main():
    # begin by running bash script
    print("Running BASH sys checks...")
    subprocess.run(['./apache_install.sh'])

    # run the necessary functions here
    chk_ip_addr()
    f_mk_prompt = get_web_dir()
    mk_web_dir(f_mk_prompt)

    # run conf scripts
    # check what setup is being used
    sec_prompt = input("Is this setup using TLS/SSL? y/N: ")
    
    if sec_prompt.lower().strip() == 'y':
        # run https func here
        # also run tls_ssl.py here as well
        pass
    elif sec_prompt.lower().strip() == 'n':
        print("Setting up conf file...")
        update_http_conf(HTTP, f_mk_prompt, ROOT)
    else:
        print("Please answer y or n to the question.")    

    # finally, set template
    select_template(f_mk_prompt)


if __name__ == "__main__":
    main()
