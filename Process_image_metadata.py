import exifread, sys

def check_for_MICH_copyright(path_to_image):
	import exifread
	# Open image file for reading (binary mode)
	I = open(path_to_image, 'rb')
	# Return Exif tags
	tags = exifread.process_file(I)
	if "Image Copyright" in tags:
		print(path_to_image,tags["Image Copyright"])


def pull_exif_date(path_to_image):
	# Open image file for reading (binary mode)
	f = open(path_to_image, 'rb')

	# Return Exif tags
	tags = exifread.process_file(f)
	for tag in tags:
		if "EXIF DateTimeOriginal" in tag:
			return tags[tag]


###MAIN FUNCTION###
if __name__ == "__main__":
	print(pull_exif_date(sys.argv[1]))
