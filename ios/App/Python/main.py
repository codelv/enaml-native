import os
import sys
import traceback
from import_hooks import SoLoader
sys.meta_path.append(SoLoader())

def main():
    print(sys.version)
    try:
        from atom.api import Atom, Unicode
        class Test(Atom):
            x = Unicode()
        t = Test()
        print(" YO DUDE IT WORKED")
    except:
        traceback.print_exc()
    print("Yay!")