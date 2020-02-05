#This script takes a folder of MICH Algae images, checks that the file name is valid for an algae image, and files it in the appropriate archive folder creating the folder if it doesn't exist.

#Image files MUST have the MICH-A- prefix, or will not be recognized as valid images to file

import Algae_utils as AU

# ~ from Algae_utils import find_if_windows_or_not
# ~ from Algae_utils import verify_algae_name_legitimate
# ~ from Algae_utils import find_valid_algae_files_in_cur_dir

###MAIN FUNCTION###
if __name__ == "__main__":	
	basedir=AU.find_if_windows_or_not()[0]
	os_type=AU.find_if_windows_or_not()[1]
	slash=AU.find_if_windows_or_not()[2]
	Algae_files,nonAlgae_files=AU.find_valid_algae_files_in_cur_dir()
	

	print(Algae_files)
	print(nonAlgae_files)

	for fil in Algae_files:
		print(fil,AU.find_appropriate_algae_archive_for_algae_file(fil))
