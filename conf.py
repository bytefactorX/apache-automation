# file to write to /etc/httpd/conf.d/x.conf file

# define constants
CONF = "/etc/httpd/conf.d"
LOG = "/var/log/httpd"

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
