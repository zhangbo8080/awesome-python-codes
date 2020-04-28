import subprocess
import time, os,re

memory_record = []
cpu_record = []


def call_adb(command):
	command_result = ''
	command_text = 'adb %s' % command
	results = os.popen(command_text, "r")
	while 1:
		line = results.readline()
		if not line: break
		command_result += line
	results.close()
	return command_result


def attached_devices():
	result = call_adb("devices")
	devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
	return [device for device in devices if len(device) > 2]


def get_men(pkg_name):
	cmd = "adb shell  dumpsys  meminfo {}".format(pkg_name)
	temp = []
	m = []
	n = []
	men_s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
	# keyword_mem = "Dalvik Heap[\s\xA0]+[0-9]*"
	# searchResult_mem = re.search(keyword_mem, str)
	# if searchResult_mem != None:
	# 	memSizeLine = searchResult_mem.group()
	# 	memSize = re.findall(r'\d+\.?\d*', memSizeLine)[0]

	for info in men_s:
		temp.append(info.split())
	m.append(temp)
	for x in m[0]:
		if x and x[0].decode() == 'TOTAL' and x[1].decode() != 'Dirty':
			n.append(x[1].decode())
			break
	if n!=[]:
		memory_record.append(int(n[0]))
		print('当前{}包的内存使用情况为---{}'.format(pkg_name, n[0]))
	else:
		print('当前{}没有占用内存的记录'.format(pkg_name))

def top_cpu(pkg_name):
	result = 0
	cmd = "adb shell dumpsys cpuinfo {}".format(pkg_name)
	temp = []
	# cmd = "adb shell top -n %s -s cpu | grep %s$" %(str(times), pkg_name)
	top_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
	cpu_info = top_info[-1].decode().split(' ')[0]
	cpu_record.append(float(cpu_info[:-1]))
	print('当前{}包的CPU使用情况为---{}'.format(pkg_name, cpu_info))


if __name__ == '__main__':
	if len(attached_devices()) != 0:
		packegName = 'com.sohu.newsclient'
		for x in range(10000):
			try:
				top_cpu(packegName)
				get_men(packegName)
				print('内存最大时为---{}'.format(max(memory_record)))
				print('内存最小时为---{}'.format(min(memory_record)))
				print('CPU使用率最大时为---{}%'.format(max(cpu_record)))
				print('CPU使用率最小时为---{}%'.format(min(cpu_record)))
				print('~~~'*25)
				time.sleep(1)
			except:
				continue
	else:
		print('请确定需要测试的设备链接到了电脑！！！')
