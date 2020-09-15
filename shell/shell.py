import os
import sys
import re


while True:
    
    if'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ('$ ').encode())
        try:
            userInput = input()
        except EOFError:
            sys.exit(1)

    if userInput == "":
        continue
    if 'exit' in userInput:
        break
    if'cd' in userInput:
        dirString = userInput.split()
        if '..' in userInput:
            changeDir = '..'
        else:
            os.chdir(dirString[1])
        try:
            os.chdir(changeDir)
        except FileNotFoundError:
            pass
        continue

    
    pid = os.getpid()
    if pid == 0:
        if '>' in userInput:
            os.close(1)
            sys.stdout = open(userInput[1].strip(),"w")
            os.set_inheritable(1,True)
            
    #if command == 'exit':
    #        break
    #    if command == 'cd':
    #        if '..'
