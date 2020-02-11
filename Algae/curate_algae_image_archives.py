#This script checks that all algae images in archives are in the correct directory and have valid names for MICH algae specimens
#Should be compatible with either python 2 or 3
#Be sure to set which_extension
#Run this script while your current working directory the folder than contains the image archives you want to investigate

import re,os

#Defining user variables
which_extension="dng" #Are you curating .dng .CR2 .pdf files? Don't include the the period.
output_file="report_algae_curation.csv"


#Defining a function that checks if an image name is legitimate. It takes a string (the file name) and returns True or False
from Algae_utils import verify_algae_name_legitimate
from Algae_utils import verify_algae_file_extension
from Algae_utils import find_if_windows_or_not
from Algae_utils import find_algae_image_archive_dirs_no_library
from Algae_utils import pull_algae_barcode_digits

###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out: #Opens the output file for writing, will delete anything already called that.
		out.write("File name,Directory,Issue found\n")#Writing a header for the csv file
		
		basedir,os_type,slash=find_if_windows_or_not()#Setting some variable based in the os type
			
			
		#Idenifying which directories in the base directory are legitimate image algae archive folders
		algae_archives=find_algae_image_archive_dirs_no_library()
	
				
		#Iterate through all the files in all the valid algae archives, check if they pass as valid file names and have the correct extensions, note errors in the output file
		all_filenames_master_dict={}
		for direc in algae_archives:
			for name in os.listdir(direc):
	
				if verify_algae_name_legitimate(name)==False:
					statement="File name improperly formatted"
					print(statement+": "+name+" in directory "+direc+slash)
					out.write(name+","+direc+slash+","+statement+"\n")
				
				if verify_algae_file_extension(name,which_extension)==False:
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
				
				
		#Iterate through all the algae image archives and check if any of the images are clearly in the wrong folder, note errors in the output file
		for di in algae_archives:
			#Grab the barcode number that the folder begins with
			di_start=re.findall("[0-9]+",di)[0]
			di_length=len(di_start)

			for fi in os.listdir(di):
				if verify_algae_name_legitimate(fi)==True:
					fi_number=pull_algae_barcode_digits(fi)
					if len(fi_number)==di_length:#If the file has the correct number of digits so that it could be the same as the folder
						if di_length==6:
							if fi_number[:2]!=di_start[:2]: #And if it number of digits is 6, if the first 2 digits do not match match, it's in the wropng place and do report that error
								print(fi_number[:2],di_start[:2])
								statement = "File suspected to be misfiled"
								print(statement+": "+name+" in directory: "+direc+slash)
								out.write(fi+","+di+","+statement+"\n")
					
						elif di_length==7:
							if fi_number[:3]!=di_start[:3]: #And if it number of digits is 7, if the first 3 digits do not match match, it's in the wrong place and do report that error
								statement = "File suspected to be misfiled"
								print(statement+": "+fi+" in directory: "+di+slash)
								out.write(name+","+di+","+statement+"\n")
						else:
							print("There was an error with the name of the archive directory: "+di+" please check on this and try again")
							exit(1)						
					else: #This happends when the number of digits in the files barcode differs from that of the folder it's in, so we know it's mis-filed
						statement = "File suspected to be misfiled"
						print(statement+": "+name+" in directory: "+direc+slash)
						out.write(fi+","+di+","+statement+"\n")

						
		print("\nscript finished")
		
