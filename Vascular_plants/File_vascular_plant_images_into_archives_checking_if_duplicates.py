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
	from vascular_plant_utils import pull_exif_date
from vascular_plant_utils import find_image_archive_dirs_no_library		
from vascular_plant_utils import find_image_archive_dirs_only_library
from vascular_plant_utils import verify_name_legitimate
from vascular_plant_utils import find_if_windows_or_not


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
							statement=item +"\t"+ name_strip_prefix[:7] +",\t"+ "no" +"\t"+ "no" +"\t"+ proper_loc +"\t"+ "Duplicated in library folder: "+dup+"\t" +"\t" +"\n"
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
							os.remove(proper_loc+slash+item)s
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

		
	
