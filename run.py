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
        case "new" | "n":
            subprocess.run(["python3", "neu.py"])
        case "update" | "u":
            subprocess.run(["python3", "update.py"])
        case "view" | "v":
            subprocess.run(["streamlit", "run", "show.py"])
        case "summary" | "s":
            subprocess.run(["python3", "summary.py"])
        case _:
            print(usage)
