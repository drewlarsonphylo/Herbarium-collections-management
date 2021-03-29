#This script is not complete and is currently only a copy of the vascular plants curate script

#This script sorts through MICH Vascular plants image archives and looks for a variety of issues.
#Be sure to set which_extension
#Run this script inside the folder than contains the image archives you want to investigate
		
import re,os

#Defining user variables
which_extension="jpg" #Are you curating .dng .CR2 .pdf .jpg files? Don't include the the period.
output_file="report_curation.csv"


#Defining a function that checks if an image name is legitimate. It takes a string (the file name) and returns True or False
from fungi_utils import verify_name_legitimate_strict
from fungi_utils import verify_file_extension
from fungi_utils import find_archive_folder_for_fungi_file


###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out: #Opens the output file for writing, will delete anything already called that.
		out.write("File name,Directory,Issue found\n")#Writing a header for the csv file
				
		#Set the value for the base dir
		basedir=os.getcwd()
		
		#Checking os_type based on os.getcwd() and automatically setting it
		if "\\" in basedir: #This is indicitive of Windows path names
			print("Using Windows path names")
			os_type="windows"
			slash="\\"
		elif "/" in basedir: #This is indicitive of Linux or Mac
			print("Using Mac path names")
			os_type="mac"
			slash="/"
			
			
		#Idenifying which directories in the base directory are legitimate image archive folders
		archive_dirs={}
		files_in_basedir=os.listdir(basedir)
		for i in files_in_basedir:
			if os.path.isdir(i)==True: #If the item is a directory
				#Check if it is properly formated as a UMICH fungi image archive. Thats like: NUMBERS - NUMBERS
				if len(re.findall("[0-9]+\ \-\ [0-9]+",i))==1: #Checks if it has the right format to be an image archive folder
					archive_dirs[i]=i #If the folder is an archive, add it to the dictionary of archives
				else:
					print(i,"<<< This directory doesn't appear to be an archive and will not be curated")
					
		print("\n")
			
			
			
		#Iterate through all the files in all the archives, check if they pass as valid file names and have the correct extensions, note errors in the output file
		all_filenames_master_dict={}
		for direc in archive_dirs:
			for name in os.listdir(direc):
	
				if verify_name_legitimate_strict(name)==False:
					statement="File name improperly formatted"
					print(statement+": "+name+" in directory "+direc+slash)
					out.write(name+","+direc+slash+","+statement+"\n")
				
				if verify_file_extension(name,which_extension)==False:
					statement="File has incorrect extension"
					print(statement+": "+name+" in directory "+direc+slash)
					out.write(name+","+direc+slash+","+statement+"\n")
					
				
				#While doing that, for every file, add the name to a giant dict with all the names in it, checking if it's already in there. Report if it is, add it if it's not, note errors in the output file
				if name in all_filenames_master_dict:
					statement="File is duplicated in multiple folders"
					print(statement+": "+name+" in both "+direc+slash+" and "+all_filenames_master_dict[name]+slash)
					out.write(name+","+"both "+direc+slash+" & "+all_filenames_master_dict[name]+slash+","+statement+"\n")
				else:
					all_filenames_master_dict[name]=direc #Adding the file name to the dict
				
				
				
		#Iterate through all the image archives and check if any of the images are clearly in the wrong folder, note errors in the output file
		for direc in archive_dirs:
	#		print(direc)
			for name in os.listdir(direc):
				if find_archive_folder_for_fungi_file(name) != direc: #Checks that the file is in the folder it should be in based on its name (checking for mis-filing
					statement = "File suspected to be misfiled"
					print(statement+": "+name+" in directory: "+direc+slash)
					out.write(name+","+direc+","+statement+"\n")
		
	
		print("\nscript finished")
		
	
