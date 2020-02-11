#This script takes in an csv with two columns. The first is a list of old file names that have been manually curated to the corresponding name in the second column.
#If the csv indicates that the 
#If saving the list from excel, be sure to save using "Comma seperated values" and NOT "CSV UTF-8 Comma Delimited"

#The csv should be formatted as follows:
#     737823-01,Deleted
#     737823-02,737823
#     737824-01,737824
#     737824-02,Deleted
#     737825-01,737825
#     737825-02,Deleted
#     737826-01,737826



import os,sys,re
from Algae_utils import find_if_windows_or_not
from Algae_utils import validate_file_extension_matches


###User variables
run_as_test=True
ext=".CR2" #Setting the  extension you want to have. Include the period
#inputfile="NameChanges.csv"
inputfile="../Name-examples.csv"
outputfile="Change_name_report.txt"
prefix="MICH-A-" #Specify here what comes before the barcodes. 
delete_file="Deleted" #The notation used to specify which files should be deleted in the csv


#Setting some variable based in the os type
basedir,os_type,slash=find_if_windows_or_not()



#print matching_files
				
with open(inputfile,"r") as filestomove:
	with open(outputfile,"w+") as out:
		
		#Make a list of all the files with the extension you have requested
		allfiles=os.listdir(basedir)
		matching_files=[]
		for i in allfiles:
			if validate_file_extension_matches(i,ext)==True:
				matching_files+=[i]	
			else:
				if i !=outputfile:
					statement="The file "+i+" does not appear to have the correct extension and so was ignored"
					print(statement)
					out.write(statement+"\n")
		
		#Iterate through all of the lines in the input file and change the names as necessary		
		for line in filestomove:
			splits=line.strip().split(",")
			if len(splits)!=2:
				print("Please check that your csv has exactly two comma seperated columns. Also be sure you do NOT select UTF-8 encoding")
				exit(1)
			
			for item in matching_files:
				if splits[0] in item: #Matches if the old barcode matches that of the current file
					old_complete_filename=prefix+splits[0]+ext
					new_complete_filename=prefix+splits[1]+ext					
					if old_complete_filename==item: #If what the name should be based on the prefix, barcode, and ext is exactly the same as the filename, move it to what the new name should be
						#Checking if the file has been marked for deletion
						if splits[1]==delete_file:
							statement=old_complete_filename+" was deleted"
							print(statement)
							out.write(statement+"\n")
							if run_as_test==False:
								os.remove(old_complete_filename)
						
						else:
							statement=old_complete_filename+" was changed to "+new_complete_filename
							print(statement)
							out.write(statement+"\n")
							if run_as_test==False:
								os.rename(old_complete_filename,new_complete_filename)
						
					else:
						statement=old_complete_filename+" doesn't exactly match "+new_complete_filename+" so no changes have been made. Check on this."
						print(statement)
						out.write(statement+"\n")

		
		
