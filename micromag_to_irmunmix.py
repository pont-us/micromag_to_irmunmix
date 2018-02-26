#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Take a micromag file and render it into a form suitable for
processing by irmunmix. This consists of: finding the field and
magnetization values and extracting them from the file; ensuring that
the magnetization is monotonically increasing; and scaling the field and
magnetization values to units compatible with irmunmix. Currently
assumes modified SI unit system in the file.

By Pontus Lurcock, 2018. Released into the public domain.
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Convert micromag data to irmunmix format")
    parser.add_argument("--output_file", metavar="filename",
                        type=str, nargs=1,
                        default=None, help="output filename")
    parser.add_argument("input_file", metavar="filename",
                        type=str, nargs=1,
                        help="input filename")

    args = parser.parse_args()
    
    infile = args.input_file[0]
    outfile = args.output_file[0]
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
                # This will only match the data header of a
                # hybrid file, which contains (T) and (Am²).
                # Currently, cgs and SI files are not handled.
                reading = True
    
    with open(outfile, "w") as fh:
        for field, mag in pairs:
            if field>0.5e-3 and mag>0:
                if mag<0: mag = 0
                fh.write("%.2f\t%.3f\r\n" % (field * 1e3, mag * 1e9))
    
if __name__ == "__main__":
    main()
