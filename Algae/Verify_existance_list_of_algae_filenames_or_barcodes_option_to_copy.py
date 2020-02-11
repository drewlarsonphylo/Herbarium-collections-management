#The script takes a Target list, parses through the herbarium directory structure, and reports whether there are images for the requested specimens.
#It reports the number of hits and the file paths for each hit


# The target list can be either a list of 6 or 7 digit barcodes in which case hits will be any file in the archive with that barcode
# or the target list can  be a list of complete file names you are searching for, in which case hits will be only files in archives with that exact name
# to force searching only for complete file names use the option require_targets_to_be_valid_complete_filenames

#Run from the base directory with all the image archive folders in it
#Run like this:      /path/to/python2.7 /path/to/verify_specimen_images.py


#Importing the necessary modules to run this script
import re,os,shutil
from Algae_utils import verify_algae_name_legitimate
from Algae_utils import find_if_windows_or_not
from Algae_utils import find_algae_image_archive_dirs_no_library
from Algae_utils import pull_algae_barcode_digits

#Hardcode things|| Changed by user as needed
inputTargetPath="TargetList.txt" #The input file with a list of UMICH Image file names to search for.
output_filename="output.csv" #The name of the file that this script will output    >>>Warning, any file with this name will be overwritten by this script<<<
header=True #Change True or False depending on if you want a header line on the output file specifying the columns
include_full_filepath_names=True #True/False if you would like full file path names for any hits included in the output. If False, only the folder the image is in will be included
copy_image_hits=True #If True, all images that hit to one of the target barcodes will be copied to the folder specified below in "copy_image_directory" 
#^THIS MAY TAKE A LONG TIME FOR LARGE NUMBERS OF FILES
copy_image_directory="Target_images" #Specify what you want the folder to be called that all the images will be copied to if copy_image_hits is set to True
require_targets_to_be_valid_complete_filenames=False #If set to True, the script will verify the name of the algae file is legitimate before continuing. 
#^Don't set this to True if you would like to target a list of barcode numbers




###MAIN FUNCTION###
if __name__ == "__main__":
	
	#Making sure the output file and error file are empty before starting the script
	if output_filename in os.listdir("."):
		os.remove(output_filename)
	if "errors.txt" in os.listdir("."):
		os.remove("errors.txt")
		
	
	#Setting some variable based in the os type
	basedir,os_type,slash=find_if_windows_or_not()

	
	#Making sure the copy_image_directory exists if needed	
	if copy_image_hits==True:
		if copy_image_directory not in os.listdir("."):
			os.makedirs(copy_image_directory)
	
	
	targets={}#initalizing a dir to save all target file  into. Key is the file; the value is a list of all image file paths associated with the file name
	#Reading in the target file and saving them in a dir
	with open(inputTargetPath,"r") as tar:
		for line in tar:
			fil=line.strip()		
			if require_targets_to_be_valid_complete_filenames==True:
				#Checking if the file name is formatted correctly 
				if verify_algae_name_legitimate(fil)==False:
					print "Error, target file contains illegitimate file name. Writing the offending file name to 'errors.txt':",fil
					with open("errors.txt","a+") as err:
							err.write(fil+"\n")		
				elif verify_algae_name_legitimate(fil)==True:#If it's a valid file name save the target in the dictionary
					targets[fil]=fil
			elif require_targets_to_be_valid_complete_filenames==False: #We you aren't running with strict file names enforced, add everything in the file to the target list
				targets[fil]=fil
		
	#Generate a list of all the image dirs in the main dir
	Image_dirs=find_algae_image_archive_dirs_no_library()
	print Image_dirs
	
	#If user requested a header to the output file, output that here
	if header==True:
		head="Target,Match/no match, Number of matches,Filenames\n"
		print "\n"+head.strip()
		with open(output_filename,"a+") as out:
			out.write(head)
	
	
	
	#For each file target, find which image folder the target file(s) would be in if they exist. There may be two options in some cases because of how the images are currently stored
	#Compare the first two or three digits of the target file barcode and look through image directories with the same first digits
	for x in targets:#Iterates though all the targets
		match=0#Default to no match, this gets switched on if a match if found
		num_matches=0#Default to no matches
		list_of_output_for_target={}
		fullcode=x.split(".")[0].split("-")[-1] #Is the barcode and any other postcodes given a valid algae name
		barcode=re.findall("^[0-9]+",fullcode)[0]
		
		
		#Specifying a bunch of variables depending on whether the target has 6 or 7 digits
		if len(barcode)==6:
			targ_len=6
			first_digits=barcode[:2]
			starting_number_for_archive=str(first_digits)+"0000"
			
		elif len(barcode)==7:
			targ_len=7
			first_digits=barcode[:3]
			starting_number_for_archive=str(first_digits)+"0000"
		else:
			print("You appear to have included a file or barcode with an incorrect number of digits for a MICH algae:",x)
		
		
		
		
		for item in Image_dirs: #Looping through each of the valid algae dirs for each target specified in the input file		
			if starting_number_for_archive == item.split(" - ")[0]: #A match means that this dir needs to be searched for one or more targets
				for fil in os.listdir(item):
					if x in fil:
						match=1
						num_matches+=1#Notes that an additional match was found
						
						
						#The path for the match will be the Image dir, plus the image file name.
						if os_type=="mac":
							if include_full_filepath_names==True: #Based on user specified value
								output_entry=str(basedir+"/"+item+"/"+fil)
							else: #User wanted the shorted path names
								output_entry=str(item+"/"+fil)
							list_of_output_for_target[output_entry]=output_entry #With either path name length, store the entry to count up later
							
						elif os_type=="windows":
							if include_full_filepath_names==True: #Based on user specified value
								output_entry=str(basedir+"\\"+item+"\\"+fil)
							else: #User wanted the shorted path names
								output_entry=str(item+"\\"+fil)
							list_of_output_for_target[output_entry]=output_entry #With either path name length, store the entry to count up later
						
						else:
							print 'You appear to have mis-specified os_type, please specify either "mac" or "windows" and try again'
							exit(1)
	
	
					
		#If after searching, output lines for each successful search OR there is no match, output that here
		if match==1:
			output_line_format=str(x)+","+str("match")+","+str(num_matches)#Initialize the output line to add file paths to
			for foundTarget in list_of_output_for_target:
				output_line_format+=","+str(foundTarget)
				
				
				#If copy_image_hits is set as True, copy the file into the directory
				if copy_image_hits==True:
					shutil.copy2(foundTarget,copy_image_directory)#This command actually does the copy of the image, copy2 preserves metadata
				
					
			output_line_format+="\n"#Add a tailing newline after all the paths have been added
			print output_line_format.strip()#not necessary
			
			with open (output_filename,"a+") as out:#Opens the output file to append more data
					out.write(output_line_format)			
			
		if match==0:
			output_line_format=str(x)+","+str("no match")+","+str(num_matches)+"\n"
			print output_line_format.strip()#not necessary
			with open (output_filename,"a+") as out:#Opens the output file to append more data
					out.write(output_line_format)
	
	print "\nscript completed"
	print "A csv of target hits was printed to",output_filename
	if copy_image_hits==True:
		print "Images of target hits were copied to the folder",copy_image_directory
	
