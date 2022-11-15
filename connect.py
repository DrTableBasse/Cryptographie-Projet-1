import os
import paramiko
import json


def connect(dns, port, user, password):
	connecting = paramiko.SSHClient()
	connecting.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# Usage env variable
	if password == "":
		connecting.connect(dns, port, user)
		print("no mdp")
	else:
		connecting.connect(dns, port, user, password)
		print("mdp")
	print("connected")
	return connecting

# Remove the error the make the remote code execution possible
def verify_folder(link, remote_path):
	_, stdout, _ = link.exec_command("cd " + remote_path)
	if stdout.channel.recv_exit_status() != 0:
		link.exec_command("mkdir " + remote_path)
		print("create folder : " + remote_path)


def send_folder(link, local_path, remote_path):
	sftp = link.open_sftp()
	for i in os.listdir(local_path):
		if not os.path.isdir(local_path + "/" + i):
			sftp.put(local_path + i, remote_path + i)
			print("send file : " + remote_path + i)
		else:
			verify_folder(link, remote_path + i)
			send_folder(link, local_path + i + "/", remote_path + i + "/")
	sftp.close()


config = json.load(open("config.json"))
ssh = connect(config["dns"], config["port"], config["user"], config["password"])
verify_folder(ssh, config["remotePath"])
send_folder(ssh, config["localPath"], config["remotePath"])
