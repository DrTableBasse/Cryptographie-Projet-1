import os
import paramiko
import json


def connect(dns, port, user, password):
	connecting = paramiko.SSHClient()
	connecting.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	if password == "":
		connecting.connect(dns, port, user)
		print("no mdp")
	else:
		connecting.connect(dns, port, user, password)
		print("mdp")
	print("connected")
	return connecting


def verify_folder(link, remotePath):
	stdin, stdout, stderr = link.exec_command("cd " + remotePath)
	if stdout.channel.recv_exit_status() != 0:
		link.exec_command("mkdir " + remotePath)
		print("create folder : " + remotePath)


def send_folder(link, localPath, remotePath):
	sftp = link.open_sftp()
	for i in os.listdir(localPath):
		if not os.path.isdir(localPath + "/" + i):
			sftp.put(localPath + i, remotePath + i)
			print("send file : " + remotePath + i)
		else:
			verify_folder(link, remotePath + i)
			send_folder(link, localPath + i + "/", remotePath + i + "/")
	sftp.close()


config = json.load(open("config.json"))
ssh = connect(config["dns"], config["port"], config["user"], config["password"])
verify_folder(ssh, config["remotePath"])
send_folder(ssh, config["localPath"], config["remotePath"])
