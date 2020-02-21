#!/usr/bin/python3
import sys,posix,time

Name='Graphical Login'
Author='NP-chaonay'
Issues='- Cannot login to user screen but always loop back to the login screen.\n\
- User appeared as already logged in without your action.'
code=None

def getUserID(user_name):
	user_entry=open('/etc/passwd').read().splitlines()
	for no in range(0,len(user_entry)):
		if user_entry[no].split(':')[0] == user_name:
			return int(user_entry[no].split(':')[3])
	return None
def finish(status) :
	if status == 'Continue':
		return
	if status == 'Complete':
		print('Troubleshooter has solved the problem completely.')
		input('Press enter to exit.')
		exit(0)
	if status == 'NoSolution':
		print('Troubleshooter hasn\'t found the solution to the problem.')
		input('Press enter to exit.')
		exit(1)
	if status == 'Cancelled':
		print('Troubleshooter has been cancelled by user.')
		input('Press enter to exit.')
		exit(0)
	if status == 'RequiredRoot':
		print('Troubleshooter requires root permission in order to continue solving the problem.')
		input('Press enter to exit.')
		exit(0)
	else:
		print('Troubleshooter hasn\'t solved the problem completely.')
		input('Press enter to exit.')
		exit(2)
def runMethod(text,function):
	print('\n### '+text+' ###')
	function()
	placeholder=('########')
	for count in range(0,len(text)):
		placeholder+='#'
	print(placeholder+'\n')
	finish(code)
def Method1():
	global code
	user_id=getUserID(input('# Type your user login ID : ')) 	
	for entry in posix.listdir('/proc/'):
		if entry.isnumeric() == True:
			if posix.stat('/proc/'+entry).st_uid == user_id:
				code='Continue'
				break
	if code == 'Continue':
		print('# Any process belonged to typed user is found.')
		while True:
			option=input('# Do you want to send signal to these processes for closing? (Y/N) : ')
			if option in ['Y','N'] :
				break
		if option == 'N':
			code='Cancelled'
			return
		else:
                        print('# Retriving processes list...')
                        pids=[]
                        for entry in posix.listdir('/proc/'):
                                if entry.isnumeric() == True:
                                        if posix.stat('/proc/'+entry).st_uid == user_id:
                                              pids.append(int(entry))
                        print('# Quitting processes...')
                        if posix.getuid() != user_id and posix.getuid() != 0:
                                print('# Error : Don\'t have enough permission. Make sure to run this troubleshooter as root.')
                                code='RequiredRoot'
                                return
                        for pid in pids:
                                posix.kill(pid, 15)
                        input('Waiting for processes to be closed properly (Recommended at 20 seconds). When ready then press enter.')
                        print('# Retriving processes list...')
                        pids=[]
                        for entry in posix.listdir('/proc/'):
                                if entry.isnumeric() == True:
                                        if posix.stat('/proc/'+entry).st_uid == user_id:
                                              pids.append(int(entry))
                        if pids:
                                while True:
                                        option=input('# There are processes not quitted by the signal. Do you want to force killing it? (Y/N) : ')
                                        if option in ['Y','N'] :
                                                break
                                if option == 'N':
                                        code='Cancelled'
                                        return
                                print('# Killing processes...')
                                for pid in pids:
                                        posix.kill(pid, 9)
                        code='Complete'
                        return
	else:
		print('# No any process belonged to typed user is found.')
		code='NoSolution'
		return

print('Linux Troubleshooter : '+Name)
print('Created by : '+Author+'\n')
if sys.platform == 'linux' :
	pass
else:
	print('Error : The current system isn\'t regular Linux system.')
	print('(Current system type is "'+sys.platform+'". Should be "linux".)')
	exit(3)

print('This troubleshooter is able to fix these issues :')
print(Issues+'\n')
while True:
	option=input('Do you want to proceed? (Y/N) : ')
	if option in ['Y','N'] :
		break
if option == 'N':
	exit(0)
print()
runMethod('Detect running processes of the user.', Method1)
