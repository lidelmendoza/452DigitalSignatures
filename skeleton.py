#I need this skeleton code is optional
import os, random, struct
import sys
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from base64 import b64encode, b64decode

##################################################
# Loads the RSA key object from the location
# @param keyPath - the path of the key
# @return - the RSA key object with the loaded key
##################################################
def loadKey(keyPath):

	# The RSA key
	key = None

	# Open the key file
	with open(keyPath, 'r') as keyFile:

		# Read the key file
		keyFileContent = keyFile.read()

		# Decode the key
		decodedKey = b64decode(keyFileContent)

		# Load the key
		key = RSA.importKey(decodedKey)

	# Return the key
	return key

##################################################
# Signs the string using an RSA private key
# @param sigKey - the signature key
# @param string - the string
##################################################
def digSig(sigKey, string):
	dataSig = sigKey.sign(string, '')
	return dataSig

##########################################################
# Returns the file signature
# @param fileName - the name of the file
# @param privKey - the private key to sign the file with
# @return fileSig - the file signature
##########################################################
def getFileSig(fileName, privKey):

	# TODO:
	# 1. Open the file
	# 2. Read the contents
	# 3. Compute the SHA-512 hash of the contents
	# 4. Sign the hash computed in 4. using the digSig() function
	# you implemented.
	# 5. Return the signed hash; this is your digital signature

    # Open the file
    with open(fileName, 'r') as tempFile:

        # Read the file
        fileContent = tempFile.read()

        # Compute the SHA-512 hash of the contents
        dataHash = SHA512.new(fileContent).hexdigest()

        # Sign the hash
        dataSignedHash = digSig(privKey, dataHash)

	return dataSignedHash

###########################################################
# Verifies the signature of the file
# @param fileName - the name of the file
# @param pubKey - the public key to use for verification
# @param signature - the signature of the file to verify
##########################################################
def verifyFileSig(fileName, pubKey, signature):

	# TODO:
	# 1. Read the contents of the input file (fileName)
	# 2. Compute the SHA-512 hash of the contents
	# 3. Use the verifySig function you implemented in
	# order to verify the file signature
	# 4. Return the result of the verification i.e.,
	# True if matches and False if it does not match

    # Read the contents of the input file
    with open(fileName, 'r') as tempFile :
        # Read the file
        fileContent = tempFile.read()

        # Compute the SHA-512 hash of the contents
        dataHash = SHA512.new(fileContent).hexdigest()

        # Verifies file signature
        if verifySig(dataHash, signature, pubKey) == True:
            return True
        else:
            return False

	pass

############################################
# Saves the digital signature to a file
# @param fileName - the name of the file
# @param signature - the signature to save
############################################
def saveSig(fileName, signature):

	# TODO:
	# Signature is a tuple with a single value.
	# Get the first value of the tuple, convert it
	# to a string, and save it to the file (i.e., indicated
	# by fileName)
	sigString = ",".join(str(i) for i in signature)
	sigFile = open(fileName, 'w')
	sigFile.write(sigString)
	sigFile.close()

	pass

###########################################
# Loads the signature and converts it into
# a tuple
# @param fileName - the file containing the
# signature
# @return - the signature
###########################################
def loadSig(fileName):

	# TODO: Load the signature from the specified file.
	# Open the file, read the signature string, convert it
	# into an integer, and then put the integer into a single
	# element tuple
	readSig = open(fileName, "r")
	sig = readSig.read()
	readSig.close()

	sigInt = int(sig)
	sigTuple = (sigInt, )

	return sigTuple

	pass

#################################################
# Verifies the signature
# @param theHash - the hash
# @param sig - the signature to check against
# @param veriKey - the verification key
# @return - True if the signature matched and
# false otherwise
#################################################
def verifySig(theHash, sig, veriKey):

	# TODO: Verify the hash against the provided
	# signature using the verify() function of the
	# key and return the result

	if veriKey.verify(theHash, sig) == True:
		return True
	else:
		return False

	pass



# The main function
def main():

	# Make sure that all the arguments have been provided
	if len(sys.argv) < 5:
		print "USAGE: " + sys.argv[0] + " <KEY FILE NAME> <SIGNATURE FILE NAME> <INPUT FILE NAME>"
		exit(-1)

	# The key file
	keyFileName = sys.argv[1]

	# Signature file name
	sigFileName = sys.argv[2]

	# The input file name
	inputFileName = sys.argv[3]

	# The mode i.e., sign or verify
	mode = sys.argv[4]

	# TODO: Load the key using the loadKey() function provided.
	key = loadKey(keyFileName)

	# We are signing
	if mode == "sign":
		sigFromFile = getFileSig(inputFileName, key)
		#       2. Save the signature to the file
		saveSig(sigFileName, sigFromFile)

		print "Signature saved to file ", sigFileName

		user_input = raw_input("Would you like to encrypt your file with AES? (Y/N)\nAnswer: ")
		if user_input.lower() == "yes" or user_input.lower() == "y":
			file = open(inputFileName, "r")

			# Check size of message to see if padding needed
			character_count = 0
			words_in_file = file.read()
			for word in words_in_file:
				for character in word:
					character_count = character_count + 1
			file.close()

			# Add padding to message
			sig = ",".join(str(i) for i in sigFromFile)
			length_of_sig = len(sig)
			total_length = character_count + length_of_sig
			if total_length % 16 != 0:
				padding = 16 - (total_length % 16)
				file = open(inputFileName, "a+")
				for i in range(0, padding - 1): # -1 for '\n'
					file.write("0")
				file.write("\n")
				file.close()

			# Add signature to message
			file = open(inputFileName, "a+")
			file.write(sig)
			file.close()

			# Find total character length in file
			'''
			file = open(inputFileName, "r")
			character_count1 = 0
			words_in_file = file.read()
			for word in words_in_file:
				for character in word:
					character_count1 = character_count1 + 1
			file.close()
			print("Character count after sig and pad: " + str(character_count1))
			'''

			# Encrypt message
			aes_key = raw_input("Please enter a 16-bit key: ")
			encryption = AES.new(aes_key, AES.MODE_CBC, "abcdef1234567890")

			file = open(inputFileName, "r")
			file_to_encrypt = file.read()
			ciphertext = encryption.encrypt(file_to_encrypt)
			file.close()

			# Write ciphertext to file
			file = open(inputFileName, "w")
			file.write(ciphertext)
			file.close()
			print(inputFileName + " has successfully been encrypted!")



	# We are verifying the signature
	elif mode == "verify":

		# TODO Use the verifyFileSig() function to check if the
		# signature signature in the signature file matches the
		# signature of the input file
		user_input = raw_input("Was your file encrypted using AES(Y/N)?\nAnswer: ")
		if user_input == "yes" or user_input == "y":
			aes_key = raw_input("Please enter the 16-bit key used to encrypt message: ")
			decryption = AES.new(aes_key, AES.MODE_CBC, "abcdef1234567890")

			# Decrypt message
			file = open(inputFileName, "r")
			file_to_decrypt = file.read()
			plaintext = decryption.decrypt(file_to_decrypt)
			file.close()

			# Write plaintext to file
			file = open(inputFileName, "w")
			file.write(plaintext)
			file.close()

			# Read lines of file into list
			file = open(inputFileName, "r")
			lines = file.readlines()
			file.close()

			# Remove padding and digital signature from file
			file = open(inputFileName, "w")
			for line in range(0, len(lines) - 2):
				file.write(lines[line])
			file.close()

		sigFromFile = loadSig(sigFileName)
		if verifyFileSig(inputFileName, key, sigFromFile) == True:
			if user_input == "yes" or user_input == "y":
				print(inputFileName + " has successfully been decrypted!")
			print("Signatures match!")
		else:
			if user_input == "yes" or user_input == "y":
				print(inputFileName + " was NOT successfully decrypted!")
			print("Signatures DO NOT match!")

		pass
	else:
		print "Invalid mode ", mode

### Call the main function ####
if __name__ == "__main__":
	main()
