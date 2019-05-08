# Assignment #3: Digital Signatures with RSA

# Members:
Lidel Mendoza (lidelmendoza9@csu.fullerton.edu)<br>
Dan Ortiz (dbortiz@csu.fullerton.edu)

# Programming Language:
Python

# How to execute program:
1. Wrtie a file you'd like to encrypt.<br>
2. Make sure you have a private and public key. <br>
3. In the terminal, format the program's execution as:<br><br>
python skeleton.py KEY_FILE_NAME SIGNATURE_FILE_NAME INPUT_FILE_NAME MODE
<br>
For KEY_FILE_NAME:<br>
* You will enter the name of the file that contains either your private or public key (depending on the mode).
<br>
For SIGNATURE_FILE_NAME:<br>
* You will enter the name of the file you wish to write the signature to.
<br>
For INPUT_FILE_NAME:<br>
* You will enter the name of the file you wish to encrypt.
<br>
For MODE:<br>
* You will either choose between SIGN (which creates the signature using the private key), or VERIFY (which verifies the signature for a file using the public key).
<br>
Example to sign: python skeleton.py privKey.pem signature.txt input_file.txt sign <br>
Example to verify: python skeleton.py pubKey.pem signature.txt input_file.txt verify

# Extra Credit:
Maybe later.

# Special Notes:
None.
