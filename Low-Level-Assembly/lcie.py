import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

verbose = False
show_mem = False

flags = sys.argv
file = flags[1]
if "-v" in flags:
    verbose = True
if "-m" in flags:
    verbose = True
    show_mem = True

a = open(file)
symbols = {}
commands = []
for idx,i in enumerate(a.read().splitlines()):
    if ":" in i:
        symbol,command = i.split(": ")
        symbols[symbol] = idx
        commands.append(command)
    else:
        commands.append(i)

current_command = ""
last_command = ""
pc = 0
acc = 0
ix = 0
compare = None

current_command = commands[pc]
while not current_command == "END":

    if show_mem:
        print()
        for idx,i in enumerate(commands):
            print(str(idx) + ": " + str(i))

    if verbose:
        input("\nCOMMAND: " + current_command + ", ADDRESS/LINE: " + str(pc) + ", ACC:" + str(acc) + ", IX:" + str(ix) + "\n")

    if current_command == "IN":
        acc = ord(str(getch())[2])
    elif current_command == "OUT":
        #print("doing out")
        print(chr(acc),end="")
        sys.stdout.flush()
        if verbose:
            print()
    else:
        #print(current_command)
        try:
            op_code,operand = current_command.split()
            if operand == "IX" or operand == "ACC":
                pass
            elif operand[0] == "#":
                if not op_code == "CMP":
                    try:
                        operand = int(operand[1:])
                    except:
                        print("\n\n=============\nSyntax Error - direct address must be int","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
                        print()
                        for idx,i in enumerate(commands):
                            print(str(idx) + ": " + str(i))
                        sys.exit()
            elif operand in symbols:
                operand = symbols[operand]
            else:
                try:
                    operand = int(operand)
                except:
                    print("\n\n=============\nSyntax Error - address must be int","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
                    print()
                    for idx,i in enumerate(commands):
                        print(str(idx) + ": " + str(i))
                    sys.exit()
        except:
            print("\n\n=============\nSyntax Error - missing operand/command doesn't exist","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
            print()
            for idx,i in enumerate(commands):
                print(str(idx) + ": " + str(i))
            sys.exit()
        if op_code == "LDM":
            acc = operand
        elif op_code == "LDI":
            acc = commands[operand]
        elif op_code == "LDX":
            acc = commands[operand + ix]
        elif op_code == "LDR":
            ix = operand
        elif op_code == "STO":
            while len(commands) < operand + 1:
                commands.append(0)
            commands[operand] = acc
        elif op_code == "STX":
            while len(commands) < operand + ix + 1:
                commands.append(0)
            commands[operand + ix] = acc
        elif op_code == "ADD":
            acc += commands[operand]
        elif op_code == "INC":
            if operand == "ACC":
                acc += 1
            if operand == "IX":
                ix += 1
        elif op_code == "DEC":
            if operand == "ACC":
                acc -= 1
            if operand == "IX":
                ix -= 1
        elif op_code == "JMP":
            pc = operand - 1
        elif op_code == "CMP":
            if "#" in operand:
                compare = acc == int(operand[1:])
            elif operand == "IX":
                compare = acc == ix
            else:
                compare = acc == commands[operand]
        elif op_code == "JPE":
            if not "CMP" in last_command:
                print("\n\n=============\nSyntax Error - CMP must proceed JPE","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
                print()
                for idx,i in enumerate(commands):
                    print(str(idx) + ": " + str(i))
                sys.exit()
            if compare:
                pc = operand - 1
        elif op_code == "JPN":
            if not "CMP" in last_command:
                print("\n\n=============\nSyntax Error - CMP must proceed JPN","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
                print()
                for idx,i in enumerate(commands):
                    print(str(idx) + ": " + str(i))
                sys.exit()
            if not compare:
                pc = operand - 1
        elif op_code == "LSL":
            acc *= 2**operand
        elif op_code == "LSR":
            acc /= 2**operand
        else:
            print("\n\n=============\nSyntax Error - Command",current_command,"doesn't exit","LINE:",pc,"COMMAND:",current_command,"ACC:",acc,"IX:",ix,"\n=============")
            print()
            for idx,i in enumerate(commands):
                print(str(idx) + ": " + str(i))
            sys.exit()
    pc += 1
    last_command = current_command
    current_command = commands[pc]
