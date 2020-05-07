import socket
 
if __name__ == '__main__':
    target = 'cc.t.sohu.com'
    targetIP = socket.gethostbyname(target)
    print ('Starting scan on host: ', targetIP)
 

    for i in range(20, 100):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((targetIP, i))
        if(result == 0) :
            print ('Port %d: OPEN' % (i,))
        s.close()
    print ('Scan is end!!!')