import os


# Function to rename multiple files
def main():
	i = '_new'
	path = 'C:/Temp/'
	for filename in os.listdir(path):
		my_dest = str(filename[:-4]) + i + '.png'
		my_source = path + filename
		my_dest = path + my_dest
		# rename() function will
		# rename all the files
		os.rename(my_source, my_dest)


# Driver Code
if __name__ == '__main__':
	# Calling main() function
	main()
