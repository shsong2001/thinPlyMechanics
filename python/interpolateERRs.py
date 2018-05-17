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
from datetime import datetime
from time import strftime
#from platform import platform
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from scipy import fftpack

def model(x,A,B,C,D):
    return (A*np.sin(B*x+C)+D)

def readData(wd,workbook,boundaryCase):
    wb = load_workbook(filename=join(wd,workbook), read_only=True)
    gIvcctWorksheet = wb['GI-VCCT']
    gIjintWorksheet = wb['GI-Jint']
    gIIvcctWorksheet = wb['GII-VCCT']
    gTOTvcctWorksheet = wb['GTOT-VCCT']
    gTOTjintWorksheet = wb['GTOT-Jint']
    czWorksheet = wb['ContactZone']
    szWorksheet = wb['SeparationZone']
    data = {}
    Vf = [0.000079,0.0001,0.2,0.3,0.4,0.5,0.55,0.6,0.65]
    Vfcolumns = {0.000079:'F',0.0001:'G',0.2:'H',0.3:'I',0.4:'J',0.5:'K',0.55:'L',0.6:'M',0.65:'N'}
    theta = [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0]
    nTheta = len(theta)
    initTheta = 4
    for c,case in enumerate(boundaryCase):
        for v,value in enumerate(Vf):
            values = []
            for n in range(0,nTheta):
                values.append(gIvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GI']['VCCT'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gIjintWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GI']['Jint'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gIIvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GII'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gTOTvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GTOT']['VCCT'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gTOTjintWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GTOT']['Jint'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(czWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['CZ'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(szWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['SZ'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
    return data

def interpolateData(outdir,data,boundaryCases):

    for c,case in enumerate(boundaryCase):
        for v,vfData in enumerate(data['GI']['VCCT'][case]):
            czStart = -1
            for a,angle in data['CZ'][case][v]['values']:
                if angle>0.0:
                    czStart = a
                    break
            filename = datetime.now().strftime('%Y-%m-%d') + '_GI-VCCT-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta'][:czStart]
            ys = vfData['values'][:czStart]
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0])
            angles = np.linspace(xs[0]-5, xs[-1]+5, num=300)
            plt.figure()
            plt.plot(data[:,0], data[:,1], 'ro')
            plt.plot(angles1, model(angles1, *res_GI), 'r-')
            plt.plot(data[:,0], data[:,2], 'bo')
            plt.plot(angles, model(angles, *res_GII), 'b-')
            plt.plot(data[:,0], data[:,3], 'go')
            plt.plot(angles, model(angles, *res_GTOT), 'g-')
            plt.xlabel('deltatheta')
            plt.ylabel('G/GO [-]')
            plt.title(titles[m])
            plt.legend(['GI,data', 'GI,interp','GII,data', 'GII,interp','GTOT,data','GTOT,interp'], loc=1)

    res_GII, cov_GII = optimize.curve_fit(model,data[:,0],data[:,2],p0=[0.7,1.0/60.0,0.0,0.0])
    res_GTOT, cov_GTOT = optimize.curve_fit(model,data[:,0],data[:,3],p0=[0.7,1.0/60.0,0.0,0.0])

    print(res_GI)
    print(res_GII)
    print(res_GTOT)

    angles = np.linspace(0., 150., num=300)
    angles1 = np.linspace(0., 60., num=120)

    plt.figure()
    plt.plot(data[:,0], data[:,1], 'ro')
    plt.plot(angles1, model(angles1, *res_GI), 'r-')
    plt.plot(data[:,0], data[:,2], 'bo')
    plt.plot(angles, model(angles, *res_GII), 'b-')
    plt.plot(data[:,0], data[:,3], 'go')
    plt.plot(angles, model(angles, *res_GTOT), 'g-')
    plt.xlabel('deltatheta')
    plt.ylabel('G/GO [-]')
    plt.title(titles[m])
    plt.legend(['GI,data', 'GI,interp','GII,data', 'GII,interp','GTOT,data','GTOT,interp'], loc=1)

    savefig('foo.png', bbox_inches='tight')

def main(argv):

    boundaryCases = ['free','geomcoupling','fixedv','fixedvlinearu']



if __name__ == "__main__":
    main(sys.argv[1:])