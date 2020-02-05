#Files images into archive folders after checking that the names are properly formatted and checking for duplicates
#Run in the base directory of the image archive. Images to file should also be in the base directory. Creates a report of what if did OR would do if running a test
#Adding a function Feb 4, 2020 where it will also check if a library format folder contains a copy of the image and won't file it if a copy already exists in those either. 

#User settings
only_test=True #When set to true, no files will be moved, when False files will be moved to their filing locations
enable_reading_metadata=False #will do nothing if overwrite is set to True;  Requires the program Exifread 2.1.2 to be installed on the machine. Allows outputing the image creation date for duplicated files
image_extension=".dng" #Include a period for the file extension
output_file="Record_of_images_filed.tsv"
overwrite_all_copy_files_with_ones_in_base_dir=False #If set to true, Image files will be filed, overwritting those that are currently in those dirs. Be careful with this.

import os,re,sys

if enable_reading_metadata==True:
	def pull_exif_date(path_to_image):
		import exifread
		# Open image file for reading (binary mode)
		f = open(path_to_image, 'rb')
		# Return Exif tags
		tags = exifread.process_file(f)
		for tag in tags:
			if "EXIF DateTimeOriginal" in tag:
				return tags[tag]
				
def find_image_archive_dirs_no_library(): #Returns a dictionary containing all the vaild image archive folders in the directory from which the script is run
	import os
	allfiles=os.listdir(".")#Generates a list of all files in the main dir
	Image_dirs={}#Initalize a dict to store names of image dirs
	for j in allfiles:#Parse through the list and find which are image dirs
		if len(re.findall("[0-9]{7}\ -\ [0-9]{7}",j))==1:#Check if the item has 7 digits followed by space - space and 7 more digits -- the format of the image dirs.
			
			#Adding an additonal check that it cant have anything other than those two chuncks of 7 digits
			if len(j)==len("1000000 - 1009999"):
				Image_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
	return Image_dirs

#Feb 4, 2020 New function to also include library dirs
def find_image_archive_dirs_only_library(): #Returns a dictionary containing all the library archive folders in the directory from which the script is run
	import os
	allfiles=os.listdir(".")#Generates a list of all files in the main dir
	Library_dirs={}#Initalize a dict to store names of image dirs
	for j in allfiles:#Parse through the list and find which are image dirs
		if len(re.findall("[0-9]{7}\ -\ [0-9]{7}",j))==1:#Check if the item has 7 digits followed by space - space and 7 more digits -- the format of the image dirs.
			
			#Adding an additonal check that it cant have anything other than those two chuncks of 7 digits
			if len(j)!=len("1000000 - 1009999"):
				Library_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
	return Library_dirs

def verify_name_legitimate(filename):
	import re
	acceptable_codes=["E","G","T","P","S"]
	if " " in filename: #This are all the criteria that we are checking for that cause the name to fail. Starting with if it has a space
		return False
	elif ")" in filename: #There can't be any parathenses is the file name
		return False
	elif "(" in filename: #There can't be any parathenses is the file name
		return False
	elif len(re.findall("(^[0-9]{7})",filename.strip("MICH-V-"))) !=1: #Fail if there isn't at least 7 consecutive numbers at the start of the file name with or without MICH-V-
		return False
	elif len(re.findall("[0-9]{8}",filename)) ==1: #Fail if there are 8 (or more) consecutive numbers at any point
		return False
	elif len(re.findall("\.",filename))>1: #Fail if there are multiple periods in the file name
		return False
	elif re.findall("[0-9]{7}[A-Z]?_?[0-9GETPS]?\.[a-zCR2]+",filename.strip("MICH-V-")) != [filename.strip("MICH-V-")]: #Fail if what follows the 7 digit barcode isn't a legitimate UMICH code. Add new accepted suffixes here
		# ^This could fail things that are acceptable when there are two underscores, need handle things smarter
		#At this point the files barcode has 7 digits
		postcode=filename.strip("MICH-V-").split(".")[0][7:] #This gives a string with only whats between the barcode and the period
		#In the rare case were there is a number immediately following an underscore and an acceptable letter variation, don't make it fail	
		#MICH-V-1234567A_E_G_1.dng
		splits=postcode.split("_")
		s_dict={}
		place=0
		has_num=False
		#The only things that should end up here fail the re above, so have multiple underscores. Therefore, the first either needs to be A-Z or empty always
		#If there is a number, it has to come last. There shouldn't ever be two Gs or two Es or two Ts
		for item in splits:
			if item in s_dict: #This means there is a repeated letter or number in postcode, which shouldn't happen. So this fails
				return False
			else:
				s_dict[item]=place #If it's not duplicated, then store in dict with value as the position, and key as the codeletter
				#Check if it's a number and flip on the switch if it is
				if item.isdigit() == True:
					if has_num==False:
						has_num=item
					elif has_num!=False: #This means there is more than one number, which is a criteria for failure
						return False
				place+=1
		#Now go through all the items in s_dict and check if they are in valid positions compared to their letters
		if "" in s_dict:
			if s_dict[""]!=0: #So if there is an empty underscore but it's not first
				return False
		elif "" not in s_dict: #This means there is no empty underscore, so there must be exactly one A-Z in position 0:
			if len(re.findall("[A-Z]",splits[0]))!=1:
				return False					
		if has_num!=False: #If there is a number, it has to come in the last position. There can only be one or it's already failed.
			if s_dict[has_num]!=len(s_dict)-1:
				return False
		#Now check that all the codes not otherwise checked are valid. There is a narrow subset of letters allowable for positions other than splits[0]. If there is a number we know
		#that it's last now and don't have to account for that.
		if has_num!=False: #This means there is a number in the last position, so don't check last position
			tocheck=splits[1:-1]
		elif has_num==False: #Also have to check the final position
			tocheck=splits[1:]
		for code in tocheck:
			if code not in acceptable_codes:
				return False	
		return True	#If the name has made it all the way through to this point in the double underscore case it is acceptable	
	else: #If the file name doesn't meet any of the criteria, don't flag it as bad
		return True
		
def find_if_windows_or_not():
	#Set the value for the base dir
	basedir=os.getcwd() 
	#Checking os_type based on os.getcwd() and automatically setting it
	if "\\" in basedir: #This is indicitive of Windows path names
		os_type="windows"
		slash="\\"
	elif "/" in basedir: #This is indicitive of Linux or Mac
		os_type="mac"
		slash="/"
	return basedir,os_type,slash


###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out:
		out.write("Filename\tBarcode\tWas filed?\tFilename issue?\tLocation to file\tDuplicated?\tDate taken of duplicate image already in folder\tDate taken of image in base directory")
		out.write("\n")
			
		#Setting variables
		basedir=find_if_windows_or_not()[0]
		os_type=find_if_windows_or_not()[1]
		slash=find_if_windows_or_not()[2]
		Image_dirs=find_image_archive_dirs_no_library()
		Library_dirs=find_image_archive_dirs_only_library()

		#Generating a list of images in the base directory that need to be filed
		list_of_images=[]
		for fil in os.listdir(basedir):
			if fil[-len(image_extension):] == image_extension: #Matches if the extension is right, now find where it should be filed
				list_of_images+=[fil]
	
		#Now move the images to the right archive location after checking that the name is valid, output the relivant infomation to the output file
		for item in list_of_images:
			
			#Check if the image name is legitimate
			if verify_name_legitimate(item)==True:
				#Find what the folder should be called that this needs to go to
				name_strip_prefix=item.strip("MICH-V-")
				firstthree=name_strip_prefix[:3]
				proper_loc=firstthree+"0000 - "+firstthree+"9999"
				duplicates_in_lib_dir={} #Assume there are no duplciates until we find some
				dont_copy_dup_in_lib_folder=False
				
				#Check if the image is copied in any of the library dirs		
				for x in Library_dirs:
						if proper_loc in x: #This means that 'x' is a Library folder that corresponds to the archive the image should go in
							#Check if the image is in the library dir
							if item in os.listdir(x):
								duplicates_in_lib_dir[x]=item #Adding that copy occurance to a list of them
							
				
				#If there a copy in any of the lib dirs, print each time this has happened, set a variable 
				if len(duplicates_in_lib_dir)!=0: #If there are library duplciates
					dont_copy_dup_in_lib_folder=True
					#Iterate through all the copies and print a statement to the file
					for dup in duplicates_in_lib_dir:
						#Report metadata if that option is on, file is duplicated
						if enable_reading_metadata == True:
							datetime_existing_file=pull_exif_date(dup+slash+item)
							datetime_file_to_move=pull_exif_date(item)
							statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "no" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicated in library folder: "+dup+"\t"+ str(datetime_existing_file) +"\t"+ str(datetime_file_to_move) +"\n"
						
						elif enable_reading_metadata != True:
						#Report for duplicated file if metadata is turned off, file is duplicated
							statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "no" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicated in library folder: "+dup+ +"\t" +"\t" +"\n"
						out.write(statement)#Writing for a duplicated image no matter what else
					
				
				#Check if the item is already in the directory we are about to move it to:
				if item in os.listdir(proper_loc): #This is the case where the file is duplicated in the main archive folder
					#"Filename,Barcode,Was filed?,Filename issue?,Location filed,Duplicated?,Creation date of duplicate image already in folder,Creation date of image in base directory"			
					
					#!!!!!!!!
					#This is the case were overwritting copies is set to True:
					if overwrite_all_copy_files_with_ones_in_base_dir == True: 
						statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "yes" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "yes but now overwritten" +"\t" +"\t" +"\n"
						print("Overwriting",proper_loc+slash+item)
						if only_test==False:
							os.rename(item,proper_loc+slash+item) #Overwriting
					#!!!!!!!
					
					
					#Report metadata if that option is on, file is duplicated
					elif enable_reading_metadata == True:
						datetime_existing_file=pull_exif_date(proper_loc+slash+item)
						datetime_file_to_move=pull_exif_date(item)
						statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "no" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicated in: "+proper_loc +"\t"+ str(datetime_existing_file) +"\t"+ str(datetime_file_to_move) +"\n"
					
					elif enable_reading_metadata != True:
					#Report for duplicated file if metadata is turned off, file is duplicated
						statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "no" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicated in"+proper_loc +"\t" +"\t" +"\n"
					out.write(statement)#Writing for a duplicated image no matter what else
					
				
				elif dont_copy_dup_in_lib_folder==True: #This means that error messages have already been output for duplcated files above, so don'y copy, but nothing to output or do now:
				#The only thing to do here is to still allow the overwitting. If enabled, it will write something to the proper archive even if there are copies in lib folders
				#If overwritting is not on, don't do anything here
					#!!!!!!!!
					#This is the case were overwritting copies is set to True:
					if overwrite_all_copy_files_with_ones_in_base_dir == True: 
						statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "yes" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicate in library folder but written anyway" +"\t" +"\t" +"\n"
						print("Filing despite duplicate in library folder",proper_loc+slash+item)
						if only_test==False:
							os.rename(item,proper_loc+slash+item) #Overwriting
				
				
				else: #This is the case where there are no issues and the file is ready to be moved
					out.write(item +"\t"+ name_strip_prefix[:7] +",\t"+ "yes" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "no" +"\t" +"\t" +"\n")
					
					###THIS IS WHERE MOVING WILL ACTUALLY HAPPEN### Name is legitimate && File is not in the target dir && this is not only a test
					if only_test==False:
						print("move command",item+","+proper_loc+slash+item)
						os.rename(item,proper_loc+slash+item)
							
			else:#If the name doesn't pass the test, This is the case where the name is invalid and the file isn't moved.
				out.write(item +"\t"+ "error in filename" +"\t"+ "n.a." +"\t"+ "yes" +"\t"+ "n.a." +"\t"+ "n.a." +"\t" +"\t" +"\n")

		
	
