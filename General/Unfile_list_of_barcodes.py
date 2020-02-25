#The script takes a Target list, parses through the herbarium directory structure, and unfiles anything that matches.
#It reports the number of hits and the file paths for each hit


#Importing the necessary modules to run this script
import re,os,shutil


#Hardcode things|| Changed by user as needed
inputTargetPath="TargetList.txt" #The input file with a list of MICH Image file names ro barcodes to search for.
# Examples like MICH-V-1234567_1.dng MICH-V-7654321B.CR2 --- Should be in the folder from which this script is run

output_filename="unfile_output.csv" #The name of the file that this script will output 

include_full_filepath_names=True #True/False if you would like full file path names for any hits included in the output. If False, only the folder the image is in will be included

only_test=False #Will create output but not actually move anything if set to True

unfile_directory="Unfiled_images" #Specify what you want the folder to be called that unfiled images go into




###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_filename,"w+") as out:
			
		#Set the value for the base dir
		basedir=os.getcwd()
		
		#Checking os_type based on os.getcwd() and automatically setting it
		if "\\" in basedir: #This is indicitive of Windows path names
			os_type="windows"
			slash="\\"
		elif "/" in basedir: #This is indicitive of Linux  or Mac
			os_type="mac"
			slash="/"
		
		
		
		#Making sure the unfile_directory exists if needed	
		if unfile_directory not in os.listdir("."):
			os.makedirs(unfile_directory)
		
		targets={}#initalizing a dir to save all target file  into. Key is the file; the value is a list of all image file paths associated with the file name
		#Reading in the target file and saving them in a dir
		with open(inputTargetPath,"r") as tar:
			for line in tar:
				fil=line.strip()
				targets[fil]=fil
			
			
			
		#Generate a list of all the image dirs in the main dir
		allfiles=os.listdir(".")#Generates a list of all files in the main dir
		Image_dirs={}#Initalize a dict to store names of image dirs
		for j in allfiles:#Parse through the list and find which are image dirs
			if len(re.findall("[0-9]{7}\ -\ [0-9]{7}",j))==1:#Check if the item has 7 digits followed by space - space and 7 more digits -- the format of the image dirs.
				Image_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
		
		
		
		#Adding the header to the output here
		head="Target,Match/no match, Number of matches,Filenames\n"
		print("\n"+head.strip())
		out.write(head)
		
		
		
		#For each file target, find which image folder the target file(s) would be in if they exist. There may be two options in some cases because of how the images are currently stored
		#Compare the first three digits of the target file barcode and look through image directories with the same three first digits
		for x in targets:#Iterates though all the targets
			match=0 #Default to no match, this gets switched on if a match if found
			num_matches=0 #Default to no matches
			list_of_output_for_target={}
			i=x.strip("MICH-AV-")
			
			for item in Image_dirs:
				if i[:3] == item[:3]: #This means the first three digits of the target barcode match the first three of the Image dir. Also matches library directories
				#A match means that this dir needs to be searched for one or more targets
					for fil in os.listdir(item):
						if x in fil:
							match=1
							num_matches+=1#Notes that an additional match was found
							
							#The path for the match will be the Image dir, plus the image file name.
							if include_full_filepath_names==True: #Based on user specified value
								output_entry=str(basedir+slash+item+slash+fil)
							else: #User wanted the shorted path names
								output_entry=str(item+slash+fil)
							list_of_output_for_target[output_entry]=output_entry #With either path name length, store the entry to count up later
							
	
						
			#If after searching, output lines for each successful search OR there is no match, output that here
			if match==1:
				output_line_format=str(x)+","+str("match")+","+str(num_matches)#Initialize the output line to add file paths to
				for foundTarget in list_of_output_for_target:
					output_line_format+=","+str(foundTarget)
					
					#If not a test, unfile the file into the unfile directory
					if only_test==False:
						shutil.move(foundTarget,unfile_directory+slash)#This command actually does the unfiling
					
				output_line_format+="\n"#Add a tailing newline after all the paths have been added
				print(output_line_format.strip())#not necessary
				out.write(output_line_format)			
				
		
		
			if match==0:
				output_line_format=str(x)+","+str("no match")+","+str(num_matches)+"\n"
				print(output_line_format.strip())#not necessary
				out.write(output_line_format)
		
			
			
		print("\nscript completed")
		print("A csv of the results was printed to",output_filename)
		if only_test==False:
			print("Target hits were moved to the folder",unfile_directory)
		
	
