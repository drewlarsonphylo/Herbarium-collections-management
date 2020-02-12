#This script just finds all of the folders in the base directory from which it is run, and returns a list of all the files in those folders

output_file="All_files_in_folders.txt"#Change this to change the output list

import os,sys

basedir=os.getcwd()

everything=os.listdir(basedir)

with open(output_file,"w+") as out:
	for i in everything:
		if os.path.isdir(i) ==True: #If the file is a folder
			for j in os.listdir(i):
				out.write(j+"\n")
