import os
import paramiko
import json
import stat


def connect(host, port, user, password):
	connecting = paramiko.SSHClient()
	connecting.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# Usage env variable
	if password == "":
		connecting.connect(host, port, user)
		print("no mdp")
	else:
		connecting.connect(host, port, user, password)
		print("mdp")
	print("connected")
	return connecting


# Remove the error the make the remote code execution possible
def verifyFolder(path, link=None):
	if link is None:
		if not os.path.isdir(path):
			os.mkdir(path)
			print("create local folder : " + path)
		else:
			print("folder local already exist : " + path)
	else:
		stdin, stdout, stderr = link.exec_command("cd " + path)
		if stdout.channel.recv_exit_status() != 0:
			link.exec_command("mkdir " + path)
			print("create remote folder : " + path)
		else:
			print("folder remote already exist : " + path)


def sendFolder(link, localPath, remotePath):
	sftp = link.open_sftp()
	for i in os.listdir(localPath):
		if not os.path.isdir(localPath + i):
			sftp.put(localPath + i, remotePath + i)
			print("send file : " + remotePath + i)
		else:
			verifyFolder(remotePath + i, link)
			sendFolder(link, localPath + i + "/", remotePath + i + "/")
	sftp.close()


def getFolder(link, localPath, remotePath):
	sftp = link.open_sftp()
	for i in sftp.listdir(remotePath):
		if not sftp.chdir(remotePath + i):
			sftp.get(remotePath + i, localPath + i)
			print("get file : " + localPath + i)
		else:
			print(localPath + i)
			verifyFolder(localPath + i)
			getFolder(link, localPath + i + "/", remotePath + i + "/")
	sftp.close()


config = json.load(open("config.json"))
ssh = connect(config["host"], config["port"], config["user"], config["password"])
verifyFolder(config["remotePath"], ssh)
# verifyFolder(config["localPath"])
# getFolder(ssh, config["localPath"], config["remotePath"])
