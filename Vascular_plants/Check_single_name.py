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
		

import sys
print verify_name_legitimate(sys.argv[1])
