#!/usr/bin/env python3

import argparse
import logging

from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname) -8s %(message)s', filename='dssat-runner.log', filemode='w')

logger = logging.getLogger(__name__)

"""
Runs dssat against a template MZX file supplied by Cheryl Porter. This MZX file is reparameterized to replace the
Weather Station input file (the .WTH string below the WSTA variable).
"""

__author__ = "Allen Lee"
__version__ = "0.1.0"
__license__ = "MIT"

def main():
    """
    for each WTH file in the input directory
    1. copy the input WTH file to conform to DSSAT standards, i.e., 8 characters. We arbitrarily changed it to MNG[\d]{5}
    where the last 5 digits are equivalent to a zero-padded string representation of the numbers after the underscore
    in the input .WTH files (treated as an ID)
    2. generate a fresh MZX file from template.mzx that references the dssat-conforming input WTH filename
    appropriately
    3. Run `DSSAT A <fresh.MZX>`
    4. Capture output and collate resulting summary.csv and stdout into a unique directory under ./results/ also named
    after the zero-padded 5 digit id
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Input data directory with weather station files to process (.WTH)",
                        default="input-data")
    args = parser.parse_args()
    path = Path(args.directory)
    if not path.is_dir():
        logger.error("%s is not a directory or does not exist, aborting.", path)
        return

    pathlist = path.glob("**/*.WTH")
    for path in pathlist:
        logger.debug("inspecting path %s in root directory %s", path, args.directory)


if __name__ == "__main__":
    main()
