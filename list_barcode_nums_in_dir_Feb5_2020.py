#Makes a list of filenames without prefixes, extensions or additional codes for the files in the directory in which it is run.

output_file_name="file_list.csv"

import os,re

file_list=os.listdir(basedir)

with open(output_file_name,"w+") as out:
	for fil in file_list:
		if "." in fil: #Making sure the file has an extension
			name=fil.split(".")[0] #grabbing everything before the dot
			name=name.strip("MICH-V-").strip("MICH-A-")
			justnumbers=re.findall("^[0-9]+",name)
			if len(justnumbers)==1: #If there is a valid barcode after stripping MICH-X-, it's a file we need to write to the output
				out.write(justnumbers[0]+","+fil+"\n")
	
