#This script is meant to allow users to check that they are able to run the Herbarium scripts
#This just returns a message and the version of python used to run the script

import os,sys

basedir=os.getcwd()

print("Script is running successfully")
print("Python version: "+sys.version)
print("Your current working directory is: "+basedir)
print("And you ran this python script with the pathname: "+sys.argv[0])
