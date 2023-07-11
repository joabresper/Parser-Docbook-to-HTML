# imports
import re

# help functions

def Request_route():
	# requests the path of the file to analyze and saves it in a variable
	pathfile = input('Enter the file path: ')
	# clean the quotes
	cleanpath = re.sub(
		r'\'|"',
		'',
		pathfile
	)
	return cleanpath.strip()
