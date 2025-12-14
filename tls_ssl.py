# script to handle all TLS/SSL processes

import subprocess

# define constants
SSLCONF = "/etc/httpd/conf.d/ssl.conf"


# run the openssl command to make key and crt
def mk_crt(f_mk_prompt):
    pass


# make backup of ssl.conf.bak
def mk_bak():
    print("Backing up ssl.conf...")
    try:
        subprocess.run(["sudo", "cp", f"{SSLCONF}", f"{SSLCONF}.bak"], check=True)
    # incase file not found
    except subprocess.CompletedProcess as e:
        print(f"Error occurred: {e}")


# try to do all major writes here if possible
def update_ssl_conf():
    pass
    

