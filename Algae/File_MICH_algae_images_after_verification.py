#This script takes a folder of MICH Algae images, checks that the file name is valid for an algae image, and files it in the appropriate archive folder creating the folder if it doesn't exist.
#It doesn't check for or otherwise consider image folders that don't have standard names like if they have been served to the library
#Compatible with python 2.x and 3.x as well as both Windows and Mac/Linux

#user defined variables
ext=".dng" #file extension you want to process, if blank you will be asked to provide this information in the command prompt
output_file="Algae_filing_report.csv" #Name out the output file that will be generated
errors="Errors.txt" #Name of the error script that will be output
only_test=False # True or False. If not set to False, this script will run, but will not create any folders or move any files. The outout file will still be created
duplicate_type_images=True #If true, the script will generate a folder called 'Duplicated_type_specimens' in the base directory, and copy all valid algae file names that have a *_T* in them

	
#Image files MUST have the MICH-A- prefix, or will not be recognized as valid images to file
import sys, os, shutil
import Algae_utils as AU


###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out: #Opening the output file for writing
		out.write("Filename,Was filed?,Appropriate archive existed?,Appropriate archive,Was a copy with exact name already in archive\n")#Writing a header line to output file
		with open(errors,"w+") as err:#Opening the error file for writing
			slash=AU.find_if_windows_or_not()[2]#Defines the slash depending if run on windows or mac/linux
			basedir=AU.find_if_windows_or_not()[0]
			
			
			#Defining file extension
			if ext=="": #if extension was left blank
				ext=AU.terminal_input_file_extension_include_dot()
			if ext[0]!=".":
				print("User defined extension is invalid, dont forget the '.' Please check on this: "+ext)
				print("exiting")
				exit(1)
		
		
			#Generating a list of all the algae files and non-algae files in the current dir
			Algae_files,nonAlgae_files=AU.find_valid_algae_files_in_cur_dir()


			#Writing error messages for all of the invalid files in the folder
			for item in nonAlgae_files: 
				ignore=[output_file,errors]
				if item not in ignore:
					err.write("Did not file "+item+" because the filename is invalid\n")
			
			
			#Duplicating all the type specimen images if desired\if duplicate_type_images==True:#Needed to duplicate types in case we need TIFFs later
			if duplicate_type_images==True:
				for X in Algae_files:
					if "_T" in X:
						if AU.validate_file_extension_matches(X,ext)!=True : #If the file extension isn't what we are looking for 
							err.write("Skipping duplication of type specimen file: "+fil+" due to incorrect extension\n")
				
						else: #Type specimen files that get here have the correct extension and are ready to be copied
							if 'Duplicated_type_specimens' not in os.listdir("."):
								os.mkdir('Duplicated_type_specimens')
						shutil.copy2(X,'Duplicated_type_specimens'+slash)#This command actually does the copy of the type image, copy2 preserves metadata
			
			
			#Iterate through all the algae files to file
			for fil in Algae_files:	
				if AU.validate_file_extension_matches(fil,ext)!=True : #If the file extension isn't what we are looking for 
					err.write("Skipping file: "+fil+" due to incorrect extension\n")
				else: #Files that get here have the correct extension and are ready to be filed having already passed as valid algae filenames earlier
					folder=AU.find_appropriate_algae_archive_for_algae_file(fil)
					
					
					#Three possible outcome at this point. 
					#1) Folder doesn't exist -> create the folder and move the image there, report
					if folder not in os.listdir("."):
		#				print("Creating folder "+folder+" and moving the file "+fil+" there")
						out.write(fil+","+"Yes"+","+"No-Created archive"+","+folder+","+"No\n")
						if only_test==False:
							#Filing the image
							os.mkdir(folder)
							os.rename(fil,folder+slash+fil)

							
					#2) Folder does exist but doesn't contain a copy of an image with the exact same name -> move image to that folder, report
					elif folder in os.listdir("."):
						if fil not in os.listdir(folder):
		#					print("Moving the file "+fil+" to folder "+folder)
							out.write(fil+","+"Yes"+","+"Yes"+","+folder+","+"No\n")
							if only_test==False:
								#Filing the image
								os.rename(fil,folder+slash+fil)
								
								
					#3) Folder does exist but does contain a copy of an image with the exact same name -> don't move the image, report
						elif fil in os.listdir(folder):
		#					print("File already in folder, doing nothing")
							out.write(fil+","+"No"+","+"Yes"+","+folder+","+"Yes\n")
					else:
						print("Directory error, exititng")
						exit(1)
		
