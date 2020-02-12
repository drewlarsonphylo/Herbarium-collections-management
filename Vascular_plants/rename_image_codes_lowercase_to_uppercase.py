#Chages file names that are *_e* to *_E* and *_g* to *_G*

only_test=False #When this is set to True, this script will print a statement for all the things would move, but will not actually change any file names
output_file="renamed_files.csv" #Name of the outout csv it makes with the old and new file names

import os,re

#Set the value for the base dir
basedir=os.getcwd()
#Checking os_type based on os.getcwd() and automatically setting it
if "\\" in basedir: #This is indicitive of Windows path names
	print("Using Windows path names")
	slash="\\"
elif "/" in basedir: #This is indicitive of Linux or Mac
	print("Using Mac path names")
	os_type="mac"
	slash="/"

#Generate a list of all the image dirs in the main dir
allfiles=os.listdir(".")#Generates a list of all files in the main dir
Image_dirs={}#Initalize a dict to store names of image dirs
for j in allfiles:#Parse through the list and find which are image dirs
	if len(re.findall("[0-9]{7}\ -\ [0-9]{7}",j))==1:#Check if the item has 7 digits followed by space - space and 7 more digits -- the format of the image dirs.
		Image_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs


#Go through each folder and rename files accordingly, print a record of what it does
with open(output_file,"w+") as out:
	for folder in Image_dirs:
		for fil in os.listdir(folder):
			
			###Additional things to replace can be added with a new .replace statement here
			newname=fil.replace("_g","_G").replace("_e","_E")
			#############################################################################
			
			if fil != newname: #These aren't the same if the file needs to be renamed
				if only_test!=True:
					print("renaming",folder+slash+fil,"to",folder+slash+newname) #Printing what is happening to the screen
					os.rename(folder+slash+fil,folder+slash+newname) #Actually doing the rename
					out.write(folder+slash+fil+","+folder+slash+newname+"\n") #Writing the old and new file name to the output file
					
				elif only_test == True:
					print("will rename",folder+slash+fil,"to",folder+slash+newname) #Printing what would have been moved to the screen
					
				
	
