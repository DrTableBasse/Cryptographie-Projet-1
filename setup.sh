#!/bin/bash

# Check if the user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Pull the repository git : https://github.com/DrTableBasse/Cryptographie-Projet-1.git
git pull https://github.com/DrTableBasse/Cryptographie-Projet-1.git

if [ ! -d "./.as_been_installed" ]
  then echo "1" > .as_been_installed
  mkdir /etc/rsa_keys/
  apt install sshpass -y
fi

# Read the file to know if the script has been run before 
if [ "$(cat .as_been_installed)" -eq 1 ]
  then echo "The script has already been run"

  # Ask to overwrite the previous installation
  read -p "Do you want to overwrite the previous installation? [y/n] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
    then echo "0" > .as_been_installed
    # Remove the value of the config file
    python3 delete_config.py
  else
    exit
  fi
fi

echo "1" > .as_been_installed

# Install python3, pip3 and all the libraries in requirements.txt
sudo apt-get update
sudo apt-get install python3 python3-pip

# Install the libraries
sudo pip3 install -r requirements.txt

# Ask the user to enter the path to the directory where the files will be stored
echo "Enter the path to the directory where the files will be stored:"
read storedPath

# Ask the user to enter the ip address of the server
echo "Enter the ip address of the server:"
read ip

# Ask the user name
echo "Enter the user name:"
read user

# Ask the user to enter password to connect in ssh
echo "Enter the password to connect in ssh:"
read password

echo "Enter the path to the directory where the files have to put to be send:"
read sendPath

# Create the directory if it doesn't exist
if [ ! -d "$storedPath" ]
    then mkdir $storedPath
fi

# Modify the config file with the user name, the ip address and the password
# File look like this:
# {
#   "host": "",
#   "port": 22,
#   "user": "",
#   "password": "",

#   "storedPath": "",
#   "sendPath": ""
# }

sed -i "s/\"host\": \"\"/\"host\": \"$ip\"/g" config.json
sed -i "s/\"user\": \"\"/\"user\": \"$user\"/g" config.json
sed -i "s/\"password\": \"\"/\"password\": \"$password\"/g" config.json


storedPath=${storedPath//\\/\\\\}
storedPath=${storedPath//&/\\&}
storedPath=${storedPath//\//\\\/}
sed -i "s/\"storedPath\": \"\"/\"storedPath\": \"parser $storedPath\"/g" config.json

sendPath=${sendPath//\\/\\\\}
sendPath=${sendPath//&/\\&}
sendPath=${sendPath//\//\\\/}
sed -i "s/\"sendPath\": \"\"/\"sendPath\": \"$sendPath\"/g" config.json
