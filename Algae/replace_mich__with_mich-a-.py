#Looks through all the files in the current working directory and changes and file name MICH_1234567.dng to MICH-A-1234567.dng

import os

basedir=os.getcwd()

for fil in os.listdir(basedir):
	if "MICH_" in fil:
		if "MICH-A-" not in fil:
			
			newname=fil.replace("MICH_","MICH-A-")
			os.rename(fil,newname)
