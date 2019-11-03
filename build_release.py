#!/usr/bin/python3

import sys
import os

sh = os.system

def get_args(): # read command shell's argument(s)
	opts = sys.argv[1:]
	argv = ""
	res = {}
	for i in opts:
		if len(argv) > 0 and "-" != i[0]:
			res.update({argv:i})
			argv = ""
		if "-" == i[0]:
			argv = i
			res.update({argv:""})
	return res

def usage():
	print("""Usage:
> ./build_release.py <-t Target_Domain> [-s,--server] [-c,--client] [-l,--linux] [-w,--windows] [-m,--macos] [-i,--i386] [-a,--amd64] [-h,--help]
""")
	sys.exit(0)

def init_go():
	sh("PATH=\\$PATH:"+sys.path[0]+"/go/bin")

def main():
	global goos, client, server, domain
	opts = get_args()
	client = False
	server = False
	goos = [None,None]
	if opts == {}:
		domain = input("Target domain: ")
	else:
		for i in opts:
			if i in ("-h","--help"):
				usage()
			elif i in ("-t","--target"):
				domain = opts[i]
			elif i in ("-c","--client"):
				client = True
			elif i in ("-s","--server"):
				server = True
			elif i in ("-i","--i386"):
				goos[1] = "386"
			elif i in ("-a","--amd64"):
				goos[1] = "amd64"
			elif i in ("-w","--windows"):
				goos[0] = "windows"
			elif i in ("-l","--linux"):
				goos[0] = "linux"
			elif i in ("-m","--macos"):
				goos[0] = "darwin"
			else:
				usage()
	if client == False and server == False:
		if input("build server?(Y/N)") in ("y","Y"):
			server = True
		if input("build client?(Y?N)") in ("y","Y"):
			client = True
	if goos == [None,None]:
		choice = input("releasing OS(win, linux, mac , default: linux):")
		if choice == "win":
			goos[0] = "windows"
		elif choice == "mac":
			goos[0] = "darwin"
		else:
			goos[0] = "linux"
		choice = input("releasing OS architechture(i386, amd64, default:amd64):")
		if choice == "i386":
			goos[1] = "386"
		else:
			goos[1] = "amd64"
	os.chdir(sys.path[0])
	bash_scripts()

def bash_scripts():
	print("generating SSL certificate")
	sh("mkdir cache")
	sh("openssl genrsa -out cache/rootCA.key 2048")
	sh("openssl req -x509 -new -nodes -key cache/rootCA.key -subj \"/CN=" + domain + "\" -days 5000 -out cache/rootCA.pem")
	sh("openssl genrsa -out cache/device.key 2048")
	sh("openssl req -new -key cache/device.key -subj \"/CN=" + domain + "\" -out cache/device.csr")
	sh("openssl x509 -req -in cache/device.csr -CA cache/rootCA.pem -CAkey cache/rootCA.key -CAcreateserial -out cache/device.crt -days 5000")
	sh("cp cache/rootCA.pem assets/client/tls/ngrokroot.crt")
	sh("cp cache/device.crt assets/server/tls/snakeoil.crt")
	sh("cp cache/device.key assets/server/tls/snakeoil.key")
	sh("rm -rf cache")
	#print("setting compiling configs")
	#sh("export GOOS="+goos[0])
	#sh("export GOARCH="+goos[1])
	print("initializing golang")
	init_go()
	config = "PATH=$PATH:"+sys.path[0]+"/go/bin\nGOPATH="+sys.path[0]+"/go GOROOT="+sys.path[0]+"/go GOOS="+goos[0]+" GOARCH="+goos[1]
	if server:
		print("building server")
		sh(config+" make release-server")
	if client:
		print("building client")
		sh(config+" make release-client")
	print("file released in ./bin")

if __name__ == "__main__":
	main()

