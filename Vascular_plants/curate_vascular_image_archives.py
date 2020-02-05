#This script sorts through MICH Vascular plants image archives and looks for a variety of issues.
#Be sure to set which_extension
#Run this script inside the folder than contains the image archives you want to investigate
		
import re,os

#Defining user variables
which_extension="CR2" #Are you curating .dng .CR2 .pdf files? Don't include the the period.
output_file="report_curation.csv"


#Defining a function that checks if an image name is legitimate. It takes a string (the file name) and returns True or False
from vascular_plant_utils import verify_name_legitimate
from vascular_plant_utils import verify_file_extension



###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out: #Opens the output file for writing, will delete anything already called that.
		out.write("File name,Directory,Issue found\n")#Writing a header for the csv file
				
		#Set the value for the base dir
		basedir=os.getcwd()
		
		#Checking os_type based on os.getcwd() and automatically setting it
		if "\\" in basedir: #This is indicitive of Windows path names
			print "Using Windows path names"
			os_type="windows"
			slash="\\"
		elif "/" in basedir: #This is indicitive of Linux or Mac
			print "Using Mac path names"
			os_type="mac"
			slash="/"
			
			
		#Idenifying which directories in the base directory are legitimate image archive folders
		archive_dirs={}
		files_in_basedir=os.listdir(basedir)
		#print files_in_basedir
		for i in files_in_basedir:
			if os.path.isdir(i)==True: #If the item is a directory
				#Check if it is properly formated as a UMICH vascular plant image archive. Thats like: 1234567 - 1234567
				if len(re.findall("[0-9]{7}\ \-\ [0-9]{7}",i))==1: #Checks if it has the right format to be an image archive folder
		#			print i,"<<< This is being treated as an archive"
					archive_dirs[i]=i #If the folder is an archive, add it to the dictionary of archives
				else:
					print i,"<<< This directory doesn't appear to be an archive and will not be curated"
					
		print "\n"
			
			
			
		#Iterate through all the files in all the archives, check if they pass as valid file names and have the correct extensions, note errors in the output file
		all_filenames_master_dict={}
		for direc in archive_dirs:
			for name in os.listdir(direc):
	
				if verify_name_legitimate(name)==False:
					statement="File name improperly formatted"
					print statement+": "+name+" in directory "+direc+slash
					out.write(name+","+direc+slash+","+statement+"\n")
				
				if verify_file_extension(name,which_extension)==False:
					statement="File has incorrect extension"
					print statement+": "+name+" in directory "+direc+slash
					out.write(name+","+direc+slash+","+statement+"\n")
					
				
				#While doing that, for every file, add the name to a giant dict with all the names in it, checking if it's already in there. Report if it is, add it if it's not, note errors in the output file
				if name in all_filenames_master_dict:
					statement="File is duplicated in multiple folders"
					print statement+": "+name+" in both "+direc+slash+" and "+all_filenames_master_dict[name]+slash
					out.write(name+","+"both "+direc+slash+" & "+all_filenames_master_dict[name]+slash+","+statement+"\n")
				else:
					all_filenames_master_dict[name]=direc #Adding the file name to the dict
				
				
				
		#Iterate through all the image archives and check if any of the images are clearly in the wrong folder, note errors in the output file
		for direc in archive_dirs:
			print "\n",direc
			for name in os.listdir(direc):
				name_strip_prefix=name.strip("MICH-V-") #Strips off the MICH-V- if it is there, and does nothing it it isn't there.
				if name_strip_prefix[:3] != direc[:3]: #If the first 3 digits of the image barcode and folder don't match, report a mis-filing
					statement = "File suspected to be misfiled"
					print statement+": "+name+" in directory: "+direc+slash
					out.write(name+","+direc+","+statement+"\n")
		
		
		print "\nscript finished"
		
	
