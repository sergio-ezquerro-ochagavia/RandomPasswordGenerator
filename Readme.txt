Random Password Generator

------------------------------------------------

Name: Random Password Generator
Version: 1.0.0
Created by: Sergio Ezquerro Ochagavía

------------------------------------------------

usage: RandPwGen.py [-h] [-times TIMES] [-length LENGTH] [-u] [-l] [-n] [-x] [-p] [-s] [-o] [-file FILE] [-v]

The script in this project generates passwords. You can run the python script file either from the command line or graphically. 

options:
  -h, --help      show this help message and exit
  -times TIMES    number of passwords to generate
  -length LENGTH  length of passwords to generate

included characters:
  -u              include uppercase characters
  -l              include lowercase characters
  -n              include numbers
  -x              include symbols

output:
  -p              print the generated passwords
  -s              save generated passwords in file
  -o              overwrite file
  -file FILE      path of file to generate
  -v, --verbose   deeper logging information

As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like        
"RandPwGen.py '@params.conf'".