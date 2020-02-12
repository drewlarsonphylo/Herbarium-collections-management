#This script just finds all of the folders in the base directory from which it is run, and returns a list of all the files in those folders

include_barcode=True #If True, in addition to the file name, the output file will also contain the 6 or 7 digit barcode in a second column of a csv
output_file="All_files_in_folders.csv"#Change this to change the output list


import os,sys,re

basedir=os.getcwd()

everything=os.listdir(basedir)

with open(output_file,"w+") as out:
	for i in everything:
		if os.path.isdir(i) ==True: #If the file is a folder
			for j in os.listdir(i):
				
				if include_barcode==True:
					barcode=re.findall("[0-9]{6,7}",j)
					if len(barcode)==1:
						out.write(j+","+barcode[0]+"\n")
				else:
					out.write(j+"\n")
