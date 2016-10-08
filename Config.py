class Config:
	## Variables:

	SearchWord = ""
	ConfigFilePath = ""
	# other variables 




	## Functions:

	# Configurator Consturctor
	def __init__(self, filepath):
		# initialize the configuration file path
		Config.ConfigFilePath = filepath


	# Actual configuration function
	#	Return 1 if successfully configured 
	#	Return 0 if any error occurs during configuration
	def config(self):
		print "TODO: Config.py Implementation."
		# Check filepath exist


		# Parse ConfigFile.xml to extract information


		return 0

	# Other functions you may need