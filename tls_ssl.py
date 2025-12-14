# script to handle all TLS/SSL processes

import subprocess

# define constants
SSLCONF = "/etc/httpd/conf.d/ssl.conf"
KEY_LOC = "/etc/pki/tls/private"
CRT_LOC = "/etc/pki/tls/certs"

# run the openssl command to make key and crt
def mk_crt(f_mk_prompt):
    print("Creating OpenSSL cert/key...")
    
    try:
        subprocess.run(f"sudo openssl req -x509 -nodes -newkey rsa:4096 -keyout {KEY_LOC}/{f_mk_prompt}.key -out {CRT_LOC}/{f_mk_prompt}.crt", shell=True, check=True)
        print("Key and cert generated successfully.")
    except subprocess.CompletedProcess as e:
        print(f"Error occurred: {e}")


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
    

