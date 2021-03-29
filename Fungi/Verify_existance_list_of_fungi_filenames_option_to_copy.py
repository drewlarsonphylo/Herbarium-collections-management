#The script takes a Target list, parses through the herbarium directory structure, and reports whether there are images for the requested specimens.
#It reports the number of hits and the file paths for each hit

#The target list can be barcodes in which case hits will be any file in the archive with that barcode
#or the target list can also be a list of complete file names you are searching for, in which case hits will be only files in archives with that exact name

#As of January 19th, 2021, you have the option to print "Date Taken" information for all target hits
#This feature uses the python library exifread, which you should be able to install with "pip3 install --user exifread"


#Run from the base directory with all the image archive folders in it
# like this:     python /path/to/verify_specimen_images.py



#Hardcode things|| Changed by user as needed
inputTargetPath="TargetList.txt" #The input file with a list of UMICH Image file names or barcodes to search for.
# Examples like MICH-V-1234567_1.dng MICH-V-7654321B.CR2 --- Should be in the folder from which this script is run

output_filename="output.csv" #The name of the file that this script will output    >>>Warning, any file with this name will be overwritten by this script<<<

header=True #Change True or False depending on if you want a header line on the output file specifying the columns

include_full_filepath_names=True #True/False if you would like full file path names for any hits included in the output. If False, only the folder the image is in will be included

copy_image_hits=False #If True, all images that hit to one of the target barcodes will be copied to the folder specified below in "copy_image_directory" 
#^THIS MAY TAKE A LONG TIME FOR LARGE NUMBERS OF FILES

copy_image_directory="Target_images" #Specify what you want the folder to be called that all the images will be copied to if copy_image_hits is set to True

print_date_taken_for_hits=False #Speify whether you want to use exifread to read photo metadata and print this in addition to path names


#Importing the necessary modules to run this script
import re,os,shutil
from fungi_utils import verify_name_legitimate
from fungi_utils import find_archive_folder_for_fungi_file
#Importing exifread if necessary
if print_date_taken_for_hits==True:
	from fungi_utils import pull_exif_date



###MAIN FUNCTION###
if __name__ == "__main__":
	
	#Making sure the output file and error file are empty before starting the script
	if output_filename in os.listdir("."):
		os.remove(output_filename)
	if "errors.txt" in os.listdir("."):
		os.remove("errors.txt")
		
	#Set the value for the base dir
	basedir=os.getcwd()
	
	#Checking os_type based on os.getcwd() and automatically setting it
	if "\\" in basedir: #This is indicitive of Windows path names
		print("Using Windows path names")
		os_type="windows"
	elif "/" in basedir: #This is indicitive of Linux  or Mac
		print("Using Mac path names")
		os_type="mac"
	
	#Making sure the copy_image_directory exists if needed	
	if copy_image_hits==True:
		if copy_image_directory not in os.listdir("."):
			os.makedirs(copy_image_directory)
	
	targets={}#initalizing a dir to save all target file  into. Key is the file; the value is a list of all image file paths associated with the file name
	#Reading in the target file and saving them in a dir
	with open(inputTargetPath,"r") as tar:
		for line in tar:
			fil=line.strip()
			
			#Checking if the file name is formatted correctly 
			if verify_name_legitimate(fil)==False:
				print("Error, target file contains illegitimate file name. Writing the offending file name to 'errors.txt':",fil)
				with open("errors.txt","a+") as err:
						err.write(fil+"\n")
						
			elif verify_name_legitimate(fil)==True:#If it's a valid file name save the target in the dictionary
				targets[fil]=fil
		
		
		
	#Generate a list of all the image dirs in the main dir
	allfiles=os.listdir(".")#Generates a list of all files in the main dir
	Image_dirs={}#Initalize a dict to store names of image dirs
	for j in allfiles:#Parse through the list and find which are image dirs
		if len(re.findall("[0-9]+\ -\ [0-9]+",j))==1:#Check if the item has digits followed by space - space and more digits -- the format of the image dirs.
			Image_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
	
	
	
	#If user requested a header to the output file, output that here
	if header==True:
		head="Target,Match/no match, Number of matches,Filenames\n"
		print("\n"+head.strip())
		with open(output_filename,"a+") as out:
			out.write(head)
	
	
	
	#For each file target, find which image folder the target file(s) would be in if they exist. There may be two options in some cases because of how the images are currently stored
	#Compare the first three digits of the target file barcode and look through image directories with the same three first digits
	for x in targets:#Iterates though all the targets
		match=0#Default to no match, this gets switched on if a match if found
		num_matches=0#Default to no matches
		list_of_output_for_target={}
		i=x.strip("MICH-F-")
		
		proper_loc=find_archive_folder_for_fungi_file(x) #proper loc is the folder this file should be stored in
		for item in Image_dirs:
			#A match means that this dir needs to be searched for one or more targets
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
						if print_date_taken_for_hits == True:
							dat=pull_exif_date(basedir+"/"+item+"/"+fil) #Uses exifread to get image taken metadata
						else:
							dat=""
						list_of_output_for_target[output_entry]=dat #With either path name length, store the entry to count up later
						
					elif os_type=="windows":
						if include_full_filepath_names==True: #Based on user specified value
							output_entry=str(basedir+"\\"+item+"\\"+fil)
						else: #User wanted the shorted path names
							output_entry=str(item+"\\"+fil)
						if print_date_taken_for_hits == True:
							dat=pull_exif_date(basedir+"\\"+item+"\\"+fil) #Uses exifread to get image taken metadata
						else:
							dat=""
						list_of_output_for_target[output_entry]=dat #With either path name length, store the entry to count up later						
					
					else:
						print('You appear to have mis-specified os_type, please specify either "mac" or "windows" and try again')
						exit(1)


					
		#If after searching, output lines for each successful search OR there is no match, output that here
		if match==1:
			
			output_line_format=str(x)+","+str("match")+","+str(num_matches)#Initialize the output line to add file paths to
			for foundTarget in list_of_output_for_target:
				if print_date_taken_for_hits == True:
					output_line_format+=","+str(foundTarget)+","+str(list_of_output_for_target[foundTarget])  #Uses the results of exifread stored from earlier
				
				else:
					output_line_format+=","+str(foundTarget)
				
				
				#If copy_image_hits is set as True, copy the file into the directory
				if copy_image_hits==True:
					shutil.copy2(foundTarget,copy_image_directory)#This command actually does the copy of the image, copy2 preserves metadata
				
				
				
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
	if copy_image_hits==True:
		print("Images of target hits were copied to the folder",copy_image_directory)
	
