#The script takes a Target list, looks through the directory inwhich it was run, and reports whether there are images for the requested specimens.
#It reports the number of hits and the file paths for each hit

# The target list can be either a list of 6 or 7 digit barcodes in which case hits will be any file in the archive with that barcode
# or the target list can  be a list of complete file names you are searching for, in which case hits will be only files in archives with that exact name

#Run from the base directory with all the image archive folders in it
#Run like this:      /path/to/python2.7 /path/to/verify_in_base_directory_existance_list_filenames_or_barcodes_option_to_move.py   
#or  python3 /path/to/verify_in_base_directory_existance_list_filenames_or_barcodes_option_to_move.py 


#Importing the necessary modules to run this script
import re,os,shutil

#Hardcode things|| Changed by user as needed
inputTargetPath="TargetList.txt" #The input file with a list of UMICH Image file names to search for.
output_filename="Output.csv" #The name of the file that this script will output    >>>Warning, any file with this name will be overwritten by this script<<<
header=True #Change True or False depending on if you want a header line on the output file specifying the columns
include_full_filepath_names=True #True/False if you would like full file path names for any hits included in the output. If False, only the folder the image is in will be included
move_image_hits=False #If True, all images that hit to one of the target barcodes will be moved to the folder specified below in "move_image_directory" 
move_image_directory="Targeted_images" #Specify what you want the folder to be called that all the images will be copied to if move_image_hits is set to True


#Defining a function to eliminate dependancies
def find_if_windows_or_not():
	import os
	basedir=os.getcwd() 
	if "\\" in basedir: #This is indicitive of Windows path names
		os_type="windows"
		slash="\\"
	elif "/" in basedir: #This is indicitive of Linux or Mac
		os_type="mac"
		slash="/"
	return basedir,os_type,slash


###MAIN FUNCTION###
if __name__ == "__main__":
	
	#Making sure the output file and error file are empty before starting the script
	if output_filename in os.listdir("."):
		os.remove(output_filename)
	if "errors.txt" in os.listdir("."):
		os.remove("errors.txt")
		
	
	#Setting some variable based in the os type
	basedir,os_type,slash=find_if_windows_or_not()

	
	#Making sure the move_image_directory exists if needed	
	if move_image_hits==True:
		if move_image_directory not in os.listdir("."):
			os.makedirs(move_image_directory)
	
	
	targets={}#initalizing a dir to save all target file  into. Key is the file; the value is a list of all image file paths associated with the file name
	#Reading in the target file and saving them in a dir
	with open(inputTargetPath,"r") as tar:
		for line in tar:
			fil=line.strip()		
			targets[fil]=fil
	
	#If user requested a header to the output file, output that here
	if header==True:
		head="Target,Match/no match, Number of matches,Filenames\n"
		print("\n"+head.strip())
		with open(output_filename,"a+") as out:
			out.write(head)
	
	#Adding all the files in the current dir to a hash for faster access
	allfiles={}
	for fil in os.listdir(basedir):
		allfiles[fil]=fil
	
	for x in targets:#Iterates though all the targets
		match=0#Default to no match, this gets switched on if a match if found
		num_matches=0#Default to no matches
		list_of_output_for_target={}
	
		for fil in allfiles: #Look through all the files
			#x is the target, want a sucessful if statement if the target barcode is the same as the file barcode, but don't want 123456 to match 1234567
			if x in fil:
				if re.findall("[0-9]{6,7}",x)==re.findall("[0-9]{6,7}",fil): #This ensures that the whole barcode number matches exactly
					match=1
					num_matches+=1#Notes that an additional match was found
					
					
					#The path for the match will be the Image dir, plus the image file name.
					if os_type=="mac":
						if include_full_filepath_names==True: #Based on user specified value
							output_entry=str(basedir+"/"+fil)
						else: #User wanted the shorted path names
							output_entry=str(fil)
						list_of_output_for_target[output_entry]=output_entry #With either path name length, store the entry to count up later
						
					elif os_type=="windows":
						if include_full_filepath_names==True: #Based on user specified value
							output_entry=str(basedir+"\\"+fil)
						else: #User wanted the shorted path names
							output_entry=str(fil)
						list_of_output_for_target[output_entry]=output_entry #With either path name length, store the entry to count up later
					
					else:
						print('You appear to have mis-specified os_type, please specify either "mac" or "windows" and try again')
						exit(1)
	
	
				else:
					print("Near match "+x+" and "+fil)
						
		#If after searching, output lines for each successful search OR there is no match, output that here
		if match==1:
			output_line_format=str(x)+","+str("match")+","+str(num_matches)#Initialize the output line to add file paths to
			for foundTarget in list_of_output_for_target:
				output_line_format+=","+str(foundTarget)
				
				
				#If move_image_hits is set as True, move the file into the directory
				if move_image_hits==True:
					shutil.move(foundTarget,move_image_directory)#This command actually does the moving of the image
				
					
			output_line_format+="\n"#Add a tailing newline after all the paths have been added
			print(output_line_format.strip())#not necessary
			
			with open (output_filename,"a+") as out:#Opens the output file to append more data
					out.write(output_line_format)			
			
		if match==0:
			output_line_format=str(x)+","+str("no match")+","+str(num_matches)+"\n"
			print(output_line_format.strip())#not necessary
			with open (output_filename,"a+") as out:#Opens the output file to append more data
					out.write(output_line_format)
	
	print("\nscript completed")
	print("A csv of target hits was printed to",output_filename)
	if move_image_hits==True:
		print("Images of target hits were moved to the folder", move_image_directory)
	
