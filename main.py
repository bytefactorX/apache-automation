#!/usr/bin/env python3

# file to handle main automation logic
# including running bash script,
# and running the two conf file scripts

import subprocess
import re
import os

# so python understands
# TODO: replace all ~ with f"{HOME}"
HOME = os.path.expanduser("~")


# manual IP address will be required 
# to ensure best practices are being exercised
def chk_ip_addr():
    INTERFACE = "ens160"

    print("Checking default interface for IPv4 method...")
    ip_method = subprocess.run(f"nmcli con show {INTERFACE} | grep ipv4.method >&/dev/null", shell=True)

    if "auto" in ip_method:
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
    print("Creating directory in home...")
    subprocess.run(f"mkdir {HOME}/{f_mk_prompt}", shell=True)

    try:
        print("Sending directory to document root...")
        subprocess.run(["cp", "-R", f"{HOME}/{f_mk_prompt}", f"/var/www/html/{f_mk_prompt}"], check=True)

        # change directory ownership to apache:apache
        subprocess.run(["sudo", "chown", "-R", "apache:apache", f"/var/www/html/{f_mk_prompt}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with subprocess: {e}")


# choose from the templates available
# and cp into the directory
def select_template(f_mk_prompt):
    temp_prompt = input("Would you like to use a CSS template? y/N: ")
    
    # if no template, insert most basic index.html file 
    # for basic access
    if temp_prompt.lower() == 'n':
        print("No template selected. Making index.html...")
        # cp to home dir first
        subprocess.run(["cp", "index.html", f"{HOME}/{f_mk_prompt}"])
        # then cp to doc root
        subprocess.run(["sudo", "cp", f"{HOME}/{f_mk_prompt}", f"/var/www/html/{f_mk_prompt}/index.html"])
        print("index.html successfully added.")
    elif temp_prompt.lower() == 'y':
        select_temp = input("Select from the following: business, blog, portfolio: ")

        # this is horrendous, but template logic is here
        if select_temp.lower() == 'business':
            pass
        elif select_temp.lower() == 'blog':
            pass
        elif select_temp.lower() == 'portfolio':
            pass
        else:
            print("Please enter a valid template type.")
    else:
        print("Please enter a valid response.")        


def main():
    # begin by running bash script
    print("Running BASH sys checks...")
    subprocess.run(['./apache_install.sh'])

    # run the necessary functions here
    chk_ip_addr()
    f_mk_prompt = get_web_dir()
    mk_web_dir(f_mk_prompt)

    # run conf scripts

    # finally, set template
    select_template(f_mk_prompt)


if __name__ == "__main__":
    main()
