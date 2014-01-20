#     Data Crawler for LUBW Measurement Stations
#     Copyright (C) 2014  Christian Rapp
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse as argp

def main():
    parser = argp.ArgumentParser(description="LUBW Data Crawler")
    parser.add_argument("-u", "--url", help="Url of the Measurement Station")
    return 0

if __name__ == "__main__":
    main()