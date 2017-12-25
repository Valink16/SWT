import netifaces
import subprocess
from threading import Thread
from time import sleep
def ask(msg,pos,neg):
	#simple neg or pos answer asking function
	#args must be string type
	loopInput=True
	while(loopInput):
		reponse=input(msg)
		if(reponse.upper()==pos.upper()):
			return True
		elif(reponse.upper()==neg.upper()):
			return False
		else:
			print("Enter {} or {}".format(pos,neg))


def log(str,returnLine=True):
	finalStr="[*]"+str
	if(returnLine):
		finalStr+="\n"
	print(finalStr,end="")

