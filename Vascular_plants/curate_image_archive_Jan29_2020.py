#This script sorts through MICH Vascular plants image archives and looks for a variety of issues.
#Be sure to set which_extension
#Run this script inside the folder than contains the image archives you want to investigate
		
import re,os

#Defining user variables
which_extension="CR2" #Are you curating .dng .CR2 .pdf files? Don't include the the period.
output_file="report_curation.csv"


#Defining a function that checks if an image name is legitimate. It takes a string (the file name) and returns True or False
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



def verify_file_extension(filename, which_extension):
	#Split the filename based on periods. The last one should be the file extension. If there are no periods, the file fails the test.
	if "." in filename:
		if filename.split(".")[-1] != which_extension:
			returnvalue=False
		else:
			returnvalue=True #If it doesn't fail an extension test, this program should return True
	else:
		returnvalue=False	
	return returnvalue



###MAIN FUNCTION###
if __name__ == "__main__":
	with open(output_file,"w+") as out: #Opens the output file for writing, will delete anything already called that.
		out.write("File name,Directory,Issue found\n")#Writing a header for the csv file
				
		#Set the value for the base dir
		basedir=os.getcwd()
		
		#Checking os_type based on os.getcwd() and automatically setting it
		if "\\" in basedir: #This is indicitive of Windows path names
			print "Using Windows path names"
			os_type="windows"
			slash="\\"
		elif "/" in basedir: #This is indicitive of Linux or Mac
			print "Using Mac path names"
			os_type="mac"
			slash="/"
			
			
		#Idenifying which directories in the base directory are legitimate image archive folders
		archive_dirs={}
		files_in_basedir=os.listdir(basedir)
		#print files_in_basedir
		for i in files_in_basedir:
			if os.path.isdir(i)==True: #If the item is a directory
				#Check if it is properly formated as a UMICH vascular plant image archive. Thats like: 1234567 - 1234567
				if len(re.findall("[0-9]{7}\ \-\ [0-9]{7}",i))==1: #Checks if it has the right format to be an image archive folder
		#			print i,"<<< This is being treated as an archive"
					archive_dirs[i]=i #If the folder is an archive, add it to the dictionary of archives
				else:
					print i,"<<< This directory doesn't appear to be an archive and will not be curated"
					
		print "\n"
			
			
			
		#Iterate through all the files in all the archives, check if they pass as valid file names and have the correct extensions, note errors in the output file
		all_filenames_master_dict={}
		for direc in archive_dirs:
			for name in os.listdir(direc):
	
				if verify_name_legitimate(name)==False:
					statement="File name improperly formatted"
					print statement+": "+name+" in directory "+direc+slash
					out.write(name+","+direc+slash+","+statement+"\n")
				
				if verify_file_extension(name,which_extension)==False:
					statement="File has incorrect extension"
					print statement+": "+name+" in directory "+direc+slash
					out.write(name+","+direc+slash+","+statement+"\n")
					
				
				#While doing that, for every file, add the name to a giant dict with all the names in it, checking if it's already in there. Report if it is, add it if it's not, note errors in the output file
				if name in all_filenames_master_dict:
					statement="File is duplicated in multiple folders"
					print statement+": "+name+" in both "+direc+slash+" and "+all_filenames_master_dict[name]+slash
					out.write(name+","+"both "+direc+slash+" & "+all_filenames_master_dict[name]+slash+","+statement+"\n")
				else:
					all_filenames_master_dict[name]=direc #Adding the file name to the dict
				
				
				
		#Iterate through all the image archives and check if any of the images are clearly in the wrong folder, note errors in the output file
		for direc in archive_dirs:
			print "\n",direc
			for name in os.listdir(direc):
				name_strip_prefix=name.strip("MICH-V-") #Strips off the MICH-V- if it is there, and does nothing it it isn't there.
				if name_strip_prefix[:3] != direc[:3]: #If the first 3 digits of the image barcode and folder don't match, report a mis-filing
					statement = "File suspected to be misfiled"
					print statement+": "+name+" in directory: "+direc+slash
					out.write(name+","+direc+","+statement+"\n")
		
		
		print "\nscript finished"
		
	
