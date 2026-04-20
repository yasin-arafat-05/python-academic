import os 
import time 

def func1():
    print("enter in func2")
    # in /bin/ls where the this command is stored;
    # also find the path using: whereis ls command in linux 
    # cat ls: will show the garble cause ls is a binary file
    # to see the actual source code: 
    """ 
    GNU is a Unix-like operating system developed as free software by the GNU Project 
    (launched by Richard Stallman in 1983) to provide users with freedom in using, 
    studying, and sharing software. Pronounced "g-noo" (a recursive acronym for "GNU's Not Unix"),
    it includes a vast collection of tools, applications, and libraries, typically paired with 
    the Linux kernel. For seeing the source code of ls command we need to download the GNU coreutils.
    Following the bellow command:
    
    # 1. Download the latest coreutils source
    wget https://ftp.gnu.org/gnu/coreutils/coreutils-9.7.tar.xz

    # 2. Extract it
    tar -xf coreutils-9.7.tar.xz

    # 3. Go to the ls source code
    cd coreutils-9.7/src

    # 4. View the main file
    cat ls.c
    # or 
    code ls.c # VS Code
    # or
    kate ls.c # Kate

    """
    os.execl("/bin/ls","ls","-lart")
    print("exit from func2")
    
print(func1())
    