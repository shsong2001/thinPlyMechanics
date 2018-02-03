#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
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


ested with Python 2.7 (64-bit) distribution in Windows 10.

'''

import sys, os
import numpy as np
from os.path import isfile, join, exists
from shutil import copyfile
import sqlite3
from datetime import datetime
from time import strftime, sleep
import timeit

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                              CSV files
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')

def appendCSVfile(dir,filename,data):
    # data is a list of lists
    # each list is written to a row
    # no check is made on data consistency
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'a') as csv:
        for row in data:
            line = ''
            for v,value in enumerate(row):
                if v>1:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                                 LOG files
#===============================================================================#

def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print('\n')

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print('===============================================================================================\n')

def writeTitleSecToLogFile(logFileFullPath,mode,title,toScreen):
    writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a',title,toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S'),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Platform: ' + platform(),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)

def writeErrorToLogFile(logFileFullPath,mode,exc,err,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
        log.write('                                     AN ERROR OCCURED\n')
        log.write('\n')
        log.write('                                -------------------------\n')
        log.write('\n')
        log.write(str(exc) + '\n')
        log.write(str(err) + '\n')
        log.write('\n')
        log.write('Terminating program\n')
        log.write('\n')
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
    if toScreen:
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')
        print('                                     AN ERROR OCCURED\n')
        print('\n')
        print('                                -------------------------\n')
        print('\n')
        print(str(exc) + '\n')
        print(str(err) + '\n')
        print('\n')
        print('Terminating program\n')
        print('\n')
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')

#===============================================================================#
#===============================================================================#
#                                Ply properties
#===============================================================================#
#===============================================================================#
def RoM(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham):
    Vm = 1 - Vf
    Gf = 0.5*ELf/(1+nuf)
    Gm = 0.5*ELm/(1+num)
    rhoc = rhof*Vf + rhom*Vm
    E1 = ELf*Vf + ELm*Vm
    E2 = 1.0/(Vf/ETf + Vm/ETm)
    nu12 = *nuf*Vf + num*Vm
    G12 = 1/(Vf/Gf + Vm/Gm)
    nu21 = nu12*(E2/E1)
    nu23 = nu12*(1 - nu21)/(1 - nu12)
    G23 = 0.5*E2)/(1 + nu23)
    alpha1 = (ELf*alphaf*Vf + ELm*alpham*Vm)/(ELf*Vf + ELm*Vm)
    alpha2 = (1 + nuf)*alphaf*Vf + (1 + num)*alpham*Vm - alpha1*nu12
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

def HalpinTsai(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham):
    Vm=1 - Vf
    Gf=dot(0.5,ELf) / (1 + nuf)
    Gm=dot(0.5,ELm) / (1 + num)
    xi=1
    rhoc=dot(rhof,Vf) + dot(rhom,Vm)
    E1=dot(ELf,Vf) + dot(ELm,Vm)
    eta1=(ETf / ETm - 1) / (ETf / ETm + dot(2,xi))
    E2=dot(ETm,(1 + dot(dot(dot(2,xi),eta1),Vf))) / (1 - dot(eta1,Vf))
    nu12=dot(nuf,Vf) + dot(num,Vm)
    eta2=(Gf / Gm - 1) / (Gf / Gm + xi)
    G12=dot(Gm,(1 + dot(dot(xi,eta2),Vf))) / (1 - dot(eta2,Vf))
    nu21=dot(nu12,(E2 / E1))
    nu23=dot(nu12,(1 - nu21)) / (1 - nu12)
    G23=dot(0.5,E2) / (1 + nu23)
    alpha1=(dot(dot(ELf,alphaf),Vf) + dot(dot(ELm,alpham),Vm)) / (dot(ELf,Vf) + dot(ELm,Vm))
    alpha2=dot(dot((1 + nuf),alphaf),Vf) + dot(dot((1 + num),alpham),Vm) - dot(alpha1,nu12)
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

def Hashin(Vf=None,rhof=None,ELf=None,ETf=None,nu12f=None,nu23f=None,alphaLf=None,alphaTf=None,rhom=None,ELm=None,ETm=None,num=None,alpham=None,*args,**kwargs):
    Vm=1 - Vf
    G12f=dot(0.5,ELf) / (1 + nu12f)
    Gm=dot(0.5,ELm) / (1 + num)
    rhoc=dot(rhof,Vf) + dot(rhom,Vm)
    kmT=dot(0.5,ELm) / (1 - num - dot(2,num ** 2))
    kfT=dot(ELf,ETf) / (dot(dot(2,ELf),(1 - nu23f)) - dot(dot(4,ETf),nu12f ** 2))
    lambda1=dot(2,(1 / Gm + Vf / kmT + Vm / kfT) ** (- 1))
    E1=dot(Vf,ELf) + dot(Vm,ELm) + dot(dot(dot(dot(2,lambda1),Vf),Vm),(num - nu12f) ** 2)
    nu12=dot(Vf,nu12f) + dot(Vm,num) + dot(dot(dot(dot(dot(0.5,lambda1),(num - nu12f)),(1 / kfT - 1 / kmT)),Vf),Vm)
    G12=Gm + Vf / (1 / (G12f - Gm) + dot(0.5,Vm) / Gm)
    K23=(dot(dot(kmT,(kfT + Gm)),Vm) + dot(dot(kfT,(kmT + Gm)),Vf)) / (dot((kfT + Gm),Vm) + dot((kmT + Gm),Vf))
    lambda3=1 + dot(4,(dot(K23,nu12 ** 2))) / E1
    G23=Gm + Vf / (1 / (dot(0.5,ETf) / (1 + nu23f) - Gm) + dot(Vm,(kmT + dot(2,Gm))) / (dot(dot(2,Gm),(kmT + Gm))))
    E2=dot(4,G23) / (1 + dot(lambda3,G23) / K23)
    nu21=dot(nu12,(E2 / E1))
    nu23=dot(nu12,(1 - nu21)) / (1 - nu12)
    km=Gm / (1 - dot(2,num))
    lambda_=(dot(0.5,(1 / Gm + Vf / km + Vm / kfT))) ** (- 1)
    alpha1=(dot(dot(ELf,alphaf),Vf) + dot(dot(ELm,alpham),Vm)) / (dot(ELf,Vf) + dot(ELm,Vm))
    alpha2=dot(- nu12,alpha1) + dot((alphaTf + dot(nu12f,alphaLf)),Vf) + dot((alpham + dot(num,alpham)),Vm) + dot(dot(dot(dot(dot(0.5,lambda_),(1 / kfT - 1 / km)),Vf),Vm),((alpham + dot(num,alpham)) - (alphaTf + dot(nu23f,alphaLf))))
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

#===============================================================================#
#===============================================================================#
#                              Laminate properties
#===============================================================================#
#===============================================================================#

def locallaminaQ(E1=None,E2=None,nu12=None,nu21=None,G12=None,*args,**kwargs):
    Q11=E1 / (1 - dot(nu12,nu21))
    Q12=dot(nu12,E2) / (1 - dot(nu12,nu21))
    Q21=copy(Q12)
    Q22=E2 / (1 - dot(nu12,nu21))
    Q66=copy(G12)
    Q=matlabarray(cat([Q11,Q12,0],[Q21,Q22,0],[0,0,Q66]))
    return Q

def locallaminaS(E1=None,E2=None,nu12=None,nu21=None,G12=None,*args,**kwargs):
    S11=1 / E1
    S12=- nu12 / E1
    S21=copy(S12)
    S22=1 / E2
    S66=copy(G12)
    S=matlabarray(cat([S11,S12,0],[S21,S22,0],[0,0,S66]))
    return S

def laminaQ(theta=None,E1=None,E2=None,nu12=None,G12=None,nu23=None,G23=None,*args,**kwargs):
    R=inv(T(theta))
    Q=dot(dot(R,locallaminaQ(E1,E2,nu12,nu21,G12)),R.T)
    return Q

def laminaS(theta=None,E1=None,E2=None,nu12=None,nu21=None,G12=None,*args,**kwargs):
    S=dot(dot(T(theta).T,locallaminaS(E1,E2,nu12,nu21,G12)),T(theta))
    return S

def CLT(throughThicknessCoords=None,angles=None,isSymmetric=None,*args,**kwargs):
    

    return A,B,D

#===============================================================================#
#===============================================================================#
#                               Transformations
#===============================================================================#
#===============================================================================#

def T(theta=None,*args,**kwargs):
    m=cos(theta) ** 2
    n=sin(theta) ** 2
    matrixT=matlabarray(cat([m ** 2,n ** 2,dot(dot(2,m),n)],[n ** 2,m ** 2,dot(dot(- 2,m),n)],[- mn,mn,m ** 2 - n ** 2]))
    return matrixT

#===============================================================================#
#===============================================================================#
#                                    MAIN
#===============================================================================#
#===============================================================================#

def main(argv):

if __name__ == "__main__":
    main(sys.argv[1:])
