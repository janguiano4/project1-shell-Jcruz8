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
    elif 'exit' in userInput:
        break
    elif'cd' in userInput:
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
    else:
        pid = os.getpid()
        dirString = userInput.split()
        if pid == 0:
            if '>' in userInput:
                os.close(1)
                sys.stdout = open(dirString[1].strip(),"w")
                os.set_inheritable(1,True)
                path(dirString[0].split())
            elif '<' in userInput:
                os.close(0)
                sys.stdout = open(dirString[1].strip(),"r")
                os.set_inheritable(0, True)
                path(dirString[0].split())
            elif '|' in userInput:
                print("hi")
                pipe1 = dirString[0].split()
                pipe2 = dirString[1].split()

                pr,pw = os.pipe()
