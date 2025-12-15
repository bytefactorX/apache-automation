# file to write to /etc/httpd/conf.d/x.conf file

# define constants
CONF = "/etc/httpd/conf.d"
LOG = "/var/log/httpd"
CRT_LOC = "/etc/pki/tls/certs"
KEY_LOC = "/etc/pki/tls/private"

# TODO: remove whitespaces and replace with tabs
def update_http_conf(HTTP, f_mk_prompt, ROOT):
    w_http = f""" 
    <VirtualHost *:{HTTP}>
      ServerName    {f_mk_prompt}
      DocumentRoot  {ROOT}/{f_mk_prompt}
      ErrorLog      {LOG}/{f_mk_prompt}.err
    </VirtualHost>
    """
    
    # write to file
    with open(f"{CONF}/{f_mk_prompt}.conf", "w") as file:
        try:
            file.write(w_http)
        # most likely to occur
        except PermissionError as e:
            print(f"Error occurred: {e}")

    print("HTTP configuration successful.")


# do the same but for https
def update_https_conf(HTTPS, f_mk_prompt, ROOT):
    w_https = f"""
    <VirtualHost *:{HTTPS}>
      ServerName    {f_mk_prompt}
      DocumentRoot  {ROOT}/{f_mk_prompt}

      SSLEngine on
      SSLCertificateFile {CRT_LOC}/{f_mk_prompt}.crt
      SSLCertificateKeyFile {KEY_LOC}/{f_mk_prompt}.key


      ErrorLog      {LOG}/{f_mk_prompt}.err
    </VirtualHost>
    """
    # write to file
    with open(f"{CONF}/{f_mk_prompt}.conf", "w") as file:
        try:
            file.write(w_https)
        # most likely to occur
        except PermissionError as e:
            print(f"Error occurred: {e}")

    print("HTTPS configuration successful.")


# use case statement to allow user to control
# which TLS/SSL protocols to use
def write_https_protocols(f_mk_prompt):
    looping = True
    tls_ssl_options = """
    TLS/SSL Options:
    TLSv1.2, TLSv1.3, or both
    """
    print(tls_ssl_options)
    
    with open(f"{CONF}/{f_mk_prompt}.conf", "r") as file:
        data = file.readlines()

    print("Choose the minimum TLS/SSL version for your HTTPS website to support.")
    tls_ssl_prompt = input("e.g. selecting TLSv1.2 will support both TLSv1.2 and TLSv1.3: ")

    while looping:
        # case statement to append to conf file
        match tls_ssl_prompt.lower().strip():
            case "tlsv1.2" | "tls 1.2" | "tls1.2":
                data[8] = "  SSLProtocol -SSLv2 -SSLv3 -TLSv1 -TLSv1.1 -TLSv1.3\n"
                looping = False
            case "tlsv1.3" | "tls 1.3" | "tls1.3":
                data[8] = "  SSLProtocol -SSLv2 -SSLv3 -TLSv1 -TLSv1.1 -TLSv1.2\n"
                looping = False
            case "both" | "tlsv1.2, tlsv1.3" | "tls1.2, tls1.3":
                # by default allows TLSv1.2 and TLSv1.3
                data[8] = "  SSLProtocol all\n"
                looping = False
            case _:
                print("Please type a valid TLS version.")

    # write the line to file
    with open(f"{CONF}/{f_mk_prompt}.conf", "w") as file:
        file.writelines(data)

    print("SSL protocols successfully configured.")        
