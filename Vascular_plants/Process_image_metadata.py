import exifread, sys

from vascular_plant_utils import check_for_MICH_copyright
from vascular_plant_utils import pull_exif_date

###MAIN FUNCTION###
if __name__ == "__main__":
	print(pull_exif_date(sys.argv[1]))
