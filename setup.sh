#!/bin/bash

# Check if the user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Install python3, pip3 and all the libraries in requirements.txt
sudo apt-get update
sudo apt-get install python3 python3-pip

# Clone the repository git
git clone https://github.com/DrTableBasse/Cryptographie-Projet-1.git
cd Cryptographie-Projet-1
sudo pip3 install -r requirements.txt

# Ask the user to enter the path to the directory where the files will be stored
echo "Enter the path to the directory where the files will be stored:"
read path

# Ask the user to enter password to connect in ssh
echo "Enter the password to connect in ssh:"
read password

# Ask the user to enter the ip address of the server
echo "Enter the ip address of the server:"
read ip

# Create the directory if it doesn't exist
if [ ! -d "$path" ]
    then mkdir $path
fi

# Ask for when the crontab should run
echo "Enter the time when the crontab should run (in minutes):"
read time

# Create the crontab
crontab -l > mycron
echo "0 * * * * cd $path" >> mycron
echo "*/$time * * * * sshpass -p $password scp * user@$ip:$path" >> mycron
crontab mycron
rm mycron
