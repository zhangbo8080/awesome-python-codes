from ws4py.client.threadedclient import WebSocketClient
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d][Level:%(levelname)s] %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def ws_connect(arg):
	try:
		ws = WebSocketClient(
			'ws://10.11.172.162:8080/demo1/websocket?S-PPID=sppid&S-PID=spid{0}&token=token&S-CID=cid{0}&S-VS=svs&User-agent=ua'.format(
				arg, arg))
		# ws = WebSocketClient(
		# 	'ws://192.168.93.16:8080/demo1/websocket?S-PPID=sppid&S-PID=spid{0}&token=token&S-CID=cid{0}&S-VS=svs&User-agent=ua'.format(
		# 		arg,arg))
		# 61.135.133.153:443
		# 192.168.93.16:8080
		ws.connect()
		logging.info("This is the #{0} connection!!!".format(arg))

		ws.run_forever()

	except KeyboardInterrupt:

		ws.close()


def thread_start(*arg):
	# create thread
	thread_list = []
	for x in range(arg[0], arg[1]):
		thread_list.append(threading.Thread(target=ws_connect, args=(x,)))

	# start thread
	for y in thread_list:
		y.start()

	for z in thread_list:
		z.join()


if __name__ == '__main__':
	thread_start(280001, 280002)
