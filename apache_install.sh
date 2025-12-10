#!/bin/bash

# run update commands prior to install
echo "Updating repo packages..."
sudo dnf update -y 


# install apache package
install_apache() {
	PACKAGE="httpd"

	# hide output & check if package is installed 
	if rpm -q $PACKAGE &>/dev/null; then
		echo "$PACKAGE is already installed."
	else
		# take user input and install as need be 
		read -p "$PACKAGE is not installed. Would you like to install? y/N: " choice
		# convert choice to lowercase
		if [[ ${choice,,} == "y" ]]; then
			echo "Installing $PACKAGE"
			sudo dnf install -y $PACKAGE
		else
			echo "Installation refused. Quitting!"
			exit 1
		fi
	fi 
}


# run systemctl command
start_service() {
	if sudo systemctl is-active httpd.service >/dev/null; then
		echo "HTTPD service already started."
	else
		sudo systemctl start httpd.service
		echo "HTTPD service has been started."
	fi
}


# install mod_ssl if user intends on using mod_ssl
install_mod_ssl() {
	MOD_SSL_PKG="mod_ssl"

	# less package checks here since mod_ssl is not required
	read -p "Do you wish to set up a website with HTTPS? (select N if already installed or will not use) y/N: " choice
	# set input to lowercase
	if [[ ${choice,,} == "y" ]]; then
	        echo "Installing $MOD_SSL_PKG"	
		sudo dnf install -y $MOD_SSL_PKG
	else
		echo "Skipping $MOD_SSL_PKG install..."
	fi
}


# add http/https to the firewall services
add_firewall() {
	FW_SERVICES=("http" "https")

	# add the services to the firewall
	for service in "${FW_SERVICES[@]}"; do
		echo "Adding $service to the Firewall..."
		sudo firewall-cmd --add-service=$service --permanent >&/dev/null
	done

	# reload the firewall to save changes
	echo "Saving Firewall changes..."
	sudo firewall-cmd --reload >/dev/null
}

# run every function
install_apache
start_service
install_mod_ssl
add_firewall
