#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime
import logging
import os
import re
import shutil
import subprocess

from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname) -8s %(message)s', filename='ming.log',
                    filemode='w')

logger = logging.getLogger(__name__)


ALL_DATA_CSV_HEADER = [
    'Grid ID', 'Latitude', 'Longitude', 'TOPWT (kg/ha)', 'HARWT (kg/ha)', 'RAIN (mm)',
]
"""
fields from summary.csv
[
'RUNNO', 'TRNO', 'R#', 'O#', 'C#', 'CR', 'MODEL', 'EXNAME', 'TNAM', 'FNAM', 'WSTA', 'SOIL_ID', 'SDAT', 'PDAT', 'EDAT',
'ADAT', 'MDAT', 'HDAT', 'DWAP', 'CWAM', 'HWAM', 'HWAH', 'BWAH', 'PWAM', 'HWUM', 'H#AM', 'H#UM', 'HIAM', 'LAIX', 'IR#M',
'IRCM', 'PRCM', 'ETCM', 'EPCM', 'ESCM', 'ROCM', 'DRCM', 'SWXM', 'NI#M', 'NICM', 'NFXM', 'NUCM', 'NLCM', 'NIAM', 'CNAM',
'GNAM', 'PI#M', 'PICM', 'PUPC', 'SPAM', 'KI#M', 'KICM', 'KUPC', 'SKAM', 'RECM', 'ONTAM', 'ONAM', 'OPTAM', 'OPAM',
'OCTAM', 'OCAM', 'DMPPM', 'DMPEM', 'DMPTM', 'DMPIM', 'YPPM', 'YPEM', 'YPTM', 'YPIM', 'DPNAM', 'DPNUM', 'YPNAM', 'YPNUM',
'NDCH', 'TMAXA', 'TMINA', 'SRADA', 'DAYLA', 'CO2A', 'PRCP', 'ETCP', 'ESCP', 'EPCP'
]
"""

DSSAT_WORK_DIR = 'dssat'  # working directory where dssat will be run with required dssat configuration + input files
BASE_RESULTS_DIR = 'results'
SENTINEL_VALUE = 'XYZZY'
TEMPLATE_FILENAME = 'template.mzx'
WTH_FILENAME_REGEX = re.compile(r"USAM8031_(?P<grid_id>\d+).WTH")

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

    pathlist = path.glob("*_[0-9]*.WTH")
    # the base results directory for this particular run
    base_results_dir = make_results_dir()
    os.makedirs(base_results_dir, exist_ok=True)
    all_data_path = Path(base_results_dir, 'all-data.csv')
    with all_data_path.open('w') as all_data:
        summary_csv = csv.writer(all_data)
        summary_csv.writerow(ALL_DATA_CSV_HEADER)
        for path in pathlist:
            process(path, base_results_dir, summary_csv)


def make_results_dir():
    today = datetime.now()
    # Organizes results by date with time subdirectories '2017-12-25/12.37'
    return os.path.join(BASE_RESULTS_DIR, today.strftime('%Y-%m-%d/%H.%M'))

def extract_grid_id(filename):
    """
    Extracts the grid id from the WTH filename USAM8031_<grid_id>.WTH and returns it as a 5 character string padded with
    zeroes along with the output file name. E.g.,
    USAM8301_1.WTH => 00001
    USAM8301_10.WTH => 00010
    10759
    """
    match = WTH_FILENAME_REGEX.match(filename)
    grid_id = format(int(match.group("grid_id")), '05d')
    output_command_filename = 'MNG{0}.MZX'.format(grid_id)
    output_weather_station_filename = 'MNG{0}.WTH'.format(grid_id)
    return grid_id, output_command_filename, output_weather_station_filename


def to_latlong(grid_id):
    lat = grid_id / 256 * -0.0002712673611110772 + 42.05166666666666
    lon = grid_id % 256 * 0.00027126736111104943 - 93.78472222222221
    return lat, lon


def _extract_output(output_path):
    extracted_output = subprocess.run(['/code/run/extract.sh', output_path.name],
                                      stdout=subprocess.PIPE, cwd=str(output_path.parent))
    parsed_output = extracted_output.stdout.decode('utf-8').rstrip()
    return parsed_output.split(' ')


def process(wth_path: Path, base_results_dir, summary_csv):
    # copy input WTH file
    wth_filename = wth_path.name
    grid_id, command_filename, weather_station_filename = extract_grid_id(wth_filename)
    template_file = Path(TEMPLATE_FILENAME)
    grid_results_dir = os.path.join(base_results_dir, grid_id)
    os.makedirs(grid_results_dir, exist_ok=True)
    # generate new command file replacing sentinel value in template.mzx with grid_id
    command_file = Path(DSSAT_WORK_DIR, command_filename)
    with template_file.open('r') as template, command_file.open('w') as out:
        for line in template:
            out.write(line.replace(SENTINEL_VALUE, grid_id))
    # copy weather station file into dssat
    weather_station_path = os.path.join(DSSAT_WORK_DIR, weather_station_filename)
    shutil.copy(str(wth_path), weather_station_path)
    # execute dssat on the new command file
    output = subprocess.run(["dssat", "A", command_filename], stdout=subprocess.PIPE, cwd=DSSAT_WORK_DIR)
    # copy generated dssat summary.csv to dedicated results directory along with all the inputs
    shutil.move(weather_station_path, grid_results_dir)
    shutil.move(os.path.join(DSSAT_WORK_DIR, "summary.csv"), grid_results_dir)
    shutil.move(str(command_file), grid_results_dir)
    output_path = Path(grid_results_dir, "output.txt")
    output_path.write_text(output.stdout.decode("utf-8"))
    # create entry in all data csv
    lat, lon = to_latlong(int(grid_id))
    topwt, harwt, rain = _extract_output(output_path)
    summary_csv.writerow([grid_id, lat, lon, topwt, harwt, rain])


if __name__ == "__main__":
    main()
