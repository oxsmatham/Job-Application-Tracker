#!/usr/bin/env python3

usage = "python3 run.py <neu|update|show>"

import subprocess
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = ""
    match arg:
        case "new":
            subprocess.run(["streamlit", "run", "neu.py"])
        case "update":
            subprocess.run(["streamlit", "run", "update.py"])
        case "show":
            subprocess.run(["streamlit", "run", "show.py"])
        case _:
            print(usage)