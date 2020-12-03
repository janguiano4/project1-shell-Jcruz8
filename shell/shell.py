import os
import sys
import re

def path(args):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    sys.exit(1)

def redirect(direction, userInput):
    userInput = userInput.split(direction)
    if direction == '>':
        os.close(1)
        sys.stdout = open(userInput[1].strip(), 'w')
        os.set_inheritable(1, True)
        path(userInput[0].split())
    else:
        os.close(0)
        sys.stdin = open(userInput[1].strip(), 'r')
        os.set_inheritable(0, True)
        path(userInput[0].split())
while True:
    
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ('$$ ').encode())
    try:
        userInput = input()
    except EOFError:
        sys.exit(1)

    if userInput == "":
        continue
    if 'exit' in userInput:
        sys.exit(0)
    if 'cd' in userInput:
        if '..' in userInput:
            changeDir = '..'
        else:
            changeDir = userInput.split('cd')[1].strip()
        try:
            os.chdir(changeDir)
        except FileNotFoundError:
            pass
        continue
    pid = os.getpid()
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        args = userInput.split()
        if "|" in args:
            pipe = userInput.split("|")
            pipeCommand1 = pipe[0].split()
            pipeCommand2 = pipe[1].split()
            pr, pw = os.pipe()
            for f in (pr, pw):
                os.set_inheritable(f, True)
            pipeFork = os.fork()
            if pipeFork < 0:
                sys.exit(1)
            if pipeFork == 0:
                os.close(1)
                os.dup(pw)
                os.set_inheritable(1, True)

                for fd in (pr, pw):
                    os.close(fd)
                path(pipeCommand1)
            else:
                os.close(0)
                os.dup(pr)
                os.set_inheritable(0, True)
                for fd in (pw, pr):
                    os.close(fd)
                path(pipeCommand2)

        if '&' in userInput:
            userInput = userInput.split('&')[0]
            args = userInput.split()

        if '>' in userInput:
            redirect('>', userInput)
        elif '<' in userInput:
            redirect('<', userInput)
        else:
            if '/' in args[0]:
                program = args[0]
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            else:
                path(args)

    else:
        if not '&' in userInput:
            os.wait()
