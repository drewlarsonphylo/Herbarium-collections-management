#The function returns True if the file name is a valid file name for michigan Algae, or False if it's not
#Defining a function that checks if an image name is legitimate. It takes a string (the file name) and returns True or False
def verify_algae_name_legitimate(filename):
	import re
	acceptable_codes=["E","T","P","S"]
	if " " in filename: #This are all the criteria that we are checking for that cause the name to fail. Starting with if it has a space
		return False
	elif ")" in filename: #There can't be any parathenses is the file name
		return False
	elif "(" in filename: #There can't be any parathenses is the file name
		return False
	elif len(re.findall("(^MICH-A-[0-9]{6})",filename)) !=1: #Fail if there isn't MICH-A- followed by at least 6 digits
		return False
	elif len(re.findall("[0-9]{8}",filename)) ==1: #Fail if there are 8 (or more) consecutive numbers at any point
		return False
	elif len(re.findall("\.",filename))!=1: #Fail if there isn't exactly one period in the file name
		return False
	elif re.findall("MICH-A-[0-9]{6,7}[A-Z]?_?[0-9GETPS]?\.[a-zCR2]+",filename) != [filename]: #Fail if what follows the 6 or 7 digit barcode isn't a legitimate MICH code. Add new accepted suffixes here
		#At this point the files barcode has 6 or 7 digits	
		fullcode=filename.split(".")[0].split("-")[-1] #Is the barcode and any other codes
		barcode=re.findall("^[0-9]+",fullcode)[0]
		if len(barcode)==7:
			postcode=fullcode[7:]
		elif len(barcode)==6:
			postcode=fullcode[6:]
		#In the rare case were there is a number immediately following an underscore and an acceptable letter variation, don't make it fail	
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
	import os
	basedir=os.getcwd() 
	if "\\" in basedir: #This is indicitive of Windows path names
		os_type="windows"
		slash="\\"
	elif "/" in basedir: #This is indicitive of Linux or Mac
		os_type="mac"
		slash="/"
	return basedir,os_type,slash
	
def find_valid_algae_files_in_cur_dir(): #This function returns two list -- one with all the valid algae names in the current dir, and one with all the non-valid algae names
	import os
	allfiles=os.listdir(".")
	algae_files=[]
	nonvalid=[]
	for f in allfiles:
		if verify_algae_name_legitimate(f)==True:
			algae_files+=[f]
		elif verify_algae_name_legitimate(f)==False:
			nonvalid+=[f]
	return algae_files,nonvalid

def pull_algae_barcode_digits(filename):
	import re
	if verify_algae_name_legitimate(filename)==True: #If true, find the barcode digits
		fullcode=filename.split(".")[0].split("-")[-1] #Is the barcode and any other postcodes given a valid algae name
		barcode=re.findall("^[0-9]+",fullcode)[0]
		return barcode
	else:
		print("Attempted to find appropriate folder for an invalid file: "+filename+"   Please fix this and try again")
		exit(1)

def find_appropriate_algae_archive_for_algae_file(filename): #Takes in an algae image file and returns the appropriate MICH archive folder name where that should be filed
	if verify_algae_name_legitimate(filename)==True: #If true, find what the archive should be
		barcode=pull_algae_barcode_digits(filename)
		if len(barcode)==6:
			appropriate_archive_name=barcode[:2]+"0000 - "+barcode[:2]+"9999"
			return appropriate_archive_name
			
		elif len(barcode)==7:
			appropriate_archive_name=barcode[:3]+"0000 - "+barcode[:3]+"9999"
			return appropriate_archive_name
		else:
			print("Barcode error, please check: "+barcode)
			exit(1)
	else:
		print("Attempted to find appropriate folder for an invalid file: "+filename+"   Please fix this and try again")
		exit(1)
		
def terminal_input_file_extension_include_dot(): #Takes no arguments, asks user for input then returns the extension the user has requested
												 #Automatically can determine if user is running python 2 or 3
	import sys
	if sys.version_info[0]==3: #Means user is running the script with python3
		extension=input("Please type the type file extension you would like to file now including the 'dot' (e.g.  .dng .CR2  .jpeg) followed by enter:  ")
		print("You have selected to file: "+extension)
		check=input("If "+extension+" is correct type 'Yes' and then enter, if it is not correct, type anything else and then enter:   ")
		if check !="Yes":
			print("Please verify which type of files you want to process and re-run using that extension")
			exit(0)
		else:
			#Checking to make sure a dot is the first character that was input
			if extension[0]!=".":
				print(extension+" does not appear to be a valid extension, did you include the '.'?")
				exit(1)
			else:
				return extension
	elif sys.version_info[0]==2: #Means user is running the script with python2
		extension=raw_input("Please type the type file extension you would like to file now including the 'dot' (e.g.  .dng .CR2  .jpeg) followed by enter:  ")
		print("You have selected to file: "+extension)
		check=raw_input("If "+extension+" is correct type 'Yes' and then enter, if it is not correct, type anything else and then enter:   ")
		if check !="Yes":
			print("Please verify which type of files you want to process and re-run using that extension")
			exit(0)
		else:
			#Checking to make sure a dot is the first character that was input
			if extension[0]!=".":
				print(extension+" does not appear to be a valid extension, did you include the '.'?")
				exit(1)
			else:
				return extension	
	else:
		print("There was an error in determining which version of python is running, exiting")
		exit(1)

def validate_file_extension_matches(filename,extension): #Give the function a filename and an extension (including dot). Returns true if they match and False if they do not match
	if filename[-len(extension):] == extension:
		return True
	else:
		return False
