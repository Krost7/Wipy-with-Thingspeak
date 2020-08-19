from network import WLAN
wlan = WLAN(mode=WLAN.STA)
import machine
import time
import gettingSensorValues as the_data
#sendig data with get mehtod
def http_get(url):
    import socket
    print(url.split('/',3))
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

nets = wlan.scan()
for net in nets:
    if net.ssid == 'kkaa':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'krostisme'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        while True:
            print(the_data.get_temp())
            temp = str(the_data.get_temp())
            humi = str(the_data.get_humi())
            http_get('https://api.thingspeak.com/update?api_key=1RH0KUK7XMOD756G&field2='+humi)
            time.sleep(15)
            http_get('https://api.thingspeak.com/update?api_key=1RH0KUK7XMOD756G&field1='+temp)

            print(humi)
            time.sleep(15)
        break
