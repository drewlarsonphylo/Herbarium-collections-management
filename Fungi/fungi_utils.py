def find_archive_folder_for_fungi_file(filename):
	import re, math
	barcode=re.findall("(^[0-9]+)",filename.replace("MICH-F-",""))[0]
	if int(barcode)<10000:
		proper_loc="1 - 9999"
	else:
		quotient=int(barcode)/10000
		if type(quotient)!=int: #This probably means python3 is running
			quotient=math.floor(int(barcode)/10000) #So giving the correct number in python3
		startRange=str(quotient)+"0000"
		endRange=int(startRange)+9999
		proper_loc=str(startRange)+" - "+str(endRange)
	return proper_loc

def check_for_MICH_copyright(path_to_image):
	import exifread
	# Open image file for reading (binary mode)
	I = open(path_to_image, 'rb')
	# Return Exif tags
	tags = exifread.process_file(I)
	if "Image Copyright" in tags:
		print(path_to_image,tags["Image Copyright"])


def pull_exif_date(path_to_image):
	import exifread
	# Open image file for reading (binary mode)
	f = open(path_to_image, 'rb')
	# Return Exif tags
	tags = exifread.process_file(f)
	for tag in tags:
		if "EXIF DateTimeOriginal" in tag:
			return tags[tag]

def verify_name_legitimate(filename):
	import re
	acceptable_codes=["E","G","T","P","S"]
	if " " in filename: #This are all the criteria that we are checking for that cause the name to fail. Starting with if it has a space
		return False
	elif ")" in filename: #There can't be any parathenses is the file name
		return False
	elif "(" in filename: #There can't be any parathenses is the file name
		return False
	elif len(re.findall("(^[0-9]+)",filename.replace("MICH-F-",""))) !=1: #Fail if there aren't consecutive numbers at the start of the file name with or without MICH-F-
		return False
	elif len(re.findall("[0-9]{8}",filename)) ==1: #Fail if there are 8 (or more) consecutive numbers at any point
		return False
	elif len(re.findall("\.",filename))>1: #Fail if there are multiple periods in the file name
		return False
	elif re.findall("[0-9]+[A-Z]?_?[0-9GETPS]?\.[a-zCR2]+",filename.replace("MICH-F-","")) != [filename.strip("MICH-F-")]: #Fail if what follows the barcode isn't a legitimate UMICH code. Add new accepted suffixes here

		barcode=re.findall("(^[0-9]+)",filename.replace("MICH-F-",""))[0]
		temp=filename.split(".")[0]
		postcode=temp.replace("MICH-F-","").replace(barcode,"")#This gives a string with only whats between the barcode and the period

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

def verify_name_legitimate_strict(filename):
	is_okbarcode=verify_name_legitimate(filename)
	if "MICH-F-"!=filename[:len("MICH-F-")]:
		is_okbarcode=False
		return is_okbarcode
	

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
	
	
def find_image_archive_dirs_no_library(): #Returns a dictionary containing all the vaild image archive folders in the directory from which the script is run
	import os,re
	allfiles=os.listdir(".")#Generates a list of all files in the main dir
	Image_dirs={}#Initalize a dict to store names of image dirs
	for j in allfiles:#Parse through the list and find which are image dirs
		if len(re.findall("[0-9]+\ -\ [0-9]+",j))==1:#Check if the item has digits followed by space - space and digits -- the format of the image dirs.
			Image_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
	return Image_dirs

#This function is an artifact of a function that used to be necessary for the vascular plant archives in 2020.
# ~ def find_image_archive_dirs_only_library(): #Returns a dictionary containing all the library archive folders in the directory from which the script is run
	# ~ #Feb 4, 2020 New function to also include library dirs
	# ~ import os,re
	# ~ allfiles=os.listdir(".")#Generates a list of all files in the main dir
	# ~ Library_dirs={}#Initalize a dict to store names of image dirs
	# ~ for j in allfiles:#Parse through the list and find which are image dirs
		# ~ if len(re.findall("[0-9]+\ -\ [0-9]+",j))==1:#Check if the item has 7 digits followed by space - space and 7 more digits -- the format of the image dirs.
			# ~ Library_dirs[j]=j#If it has the correct format, add the dir name to the dict that stores the names of the image dirs
	# ~ return Library_dirs
	
def find_if_windows_or_not():
	#Set the value for the base dir
	import os
	basedir=os.getcwd() 
	#Checking os_type based on os.getcwd() and automatically setting it
	if "\\" in basedir: #This is indicitive of Windows path names
		os_type="windows"
		slash="\\"
	elif "/" in basedir: #This is indicitive of Linux or Mac
		os_type="mac"
		slash="/"
	return basedir,os_type,slash
