#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Take a micromag file and render it into a form suitable for
processing by irmunmix.
'''

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Preprocess micromag files.")
    parser.add_argument("--output_file", metavar="filename",
                        type=str, nargs=1,
                        default=None, help="output filename")
    parser.add_argument("--scale", metavar="factor", type=str, nargs="?",
                        help="remanence scaling factor")
    parser.add_argument("input_file", metavar="filename",
                        type=str, nargs=1,
                        help="input filename")

    args = parser.parse_args()
    
    infile = args.input_file[0]
    outfile = args.output_file[0]
    header = "     (T)          (Am"
    pairs = []
    maxmag = 0
    with open(infile, "rt", encoding="iso-8859-1") as fh:
        reading = False
        for line in fh.readlines():
            if reading:
                if line.strip() == "": break
                field, mag = map(float, line.strip().split(","))
                if mag < maxmag: mag = maxmag
                else: maxmag = mag
                pairs.append((field, mag))
            if "(T)" in line and "(Am" in line:
                reading = True
    
    with open(outfile, "w") as fh:
        for field, mag in pairs:
            if field>0.5e-3 and mag>0:
                if mag<0: mag = 0
                fh.write("%.2f\t%.3f\r\n" % (field * 1e3, mag * 1e9))
    
if __name__ == "__main__":
    main()
