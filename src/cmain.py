import cinit, sys, os, subprocess, pathlib
import stdlib.__entry__ as stdlib

def main(argv):
    path = argv[0] if argv else os.getcwd()
    if path in ("--use-gcc", "--use-clang"):
        path = os.getcwd()
    attributes = argv[1:] if len(argv) >= 2 else []

    useGCC = False
    useClang = False
    for each in attributes:
        if each == "--use-gcc":
            useGCC = True
        elif each == "--use-clang":
            useClang = True
        else:
            print(f"Unknown option: {each}")
            sys.exit(1)
    
    fs = stdlib.filesystem()
    if not fs.isExistAndDir(path):
        print(f"Directory not found: {path}")
        sys.exit(1)

    cCode = cinit.packager(path)
    setupc = os.path.join(path, "_setup.c")
    setupexe = pathlib.Path(setupc).with_suffix(".exe")
    fs.createFile(setupc)
    fs.writeToFile(setupc, cCode)

    def nonRepetive(name):
        test = subprocess.Popen(f"{name} -v", shell=True)
        if test.returncode != 0:
            print(f"{name} doesn't exist")
            sys.exit(1)
        else:
            test2 = subprocess.Popen(f"{name} -c \"{setupc.replace("\\", "/")}\" -o \"{setupexe.replace("\\", "/")}\"", shell=True, text=True)
            test2.communicate()
            if test2.returncode != 0:
                print("Setup file compilation failed")
                sys.exit(1)
            os.remove(setupc.replace("\\", "/"))

    if useGCC:
        nonRepetive("gcc")

    elif useClang:
        nonRepetive("clang")

if __name__ == "__main__":
    main(sys.argv[1:])
