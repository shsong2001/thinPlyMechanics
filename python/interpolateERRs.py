#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine & Luleå tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================================

DESCRIPTION



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution in Windows 10.

'''

import sys
#import os
from os.path import isfile, join, exists
#from os import listdir, stat, makedirs
#from datetime import datetime
#from time import strftime
#from platform import platform
from openpyxl import load_workbook

def readData(wd,workbook):
    wb = load_workbook(filename=join(wd,workbook), read_only=True)
    gIvcctWorksheet = wb['GI']
    gIjintWorksheet = wb['GI']
    gIIvcctWorksheet = wb['GI']
    gTOTvcctWorksheet = wb['GI']
    gTOTjintWorksheet = wb['GI']
    czWorksheet = wb['GI']
    szWorksheet = wb['GI']

for row in ws.rows:
    for cell in row:
        print(cell.value)





if __name__ == "__main__":
    main(sys.argv[1:])
