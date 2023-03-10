#!/usr/bin/env python
import sys, re, os
import matplotlib.pyplot as plt
import numpy as np

path = sys.argv[1]
inputRF = path+"/ResponseFrequency.json"
inputEAC = path+"/EpitopeAssayCount.json"
postfix = path.split("/")[1]

# copy proper Variant position file from the given path
cmd = "cp %s/VariantPosition.py ."%(path)
os.system(cmd)
from VariantPosition import *

def drawCorr(posmin, posmax, listRF, listEAC):

    # plot 2D
    plt.scatter(listEAC[posmin-1:posmax], listRF[posmin-1:posmax], label='All (%.f)'%(len(listRF[posmin-1:posmax])))

    # filter variant
    filteredLists = {}
    colors = ['yellowgreen', 'orange']
    markers = ['o', '^']
    for vidx, variant in enumerate(variants):
        #print ("%s(#of position: %.f)"%(variant, len(variants[variant])))
        filteredLists[variant] = [[], []]
        for position in variants[variant]:
            #print (position)
            idx = position - 1
            if position>=posmin and position<=posmax:
                filteredLists[variant][0].append(listEAC[idx])
                filteredLists[variant][1].append(listRF[idx])
        plt.scatter(filteredLists[variant][0], filteredLists[variant][1], c=colors[vidx], marker=markers[vidx], label=variant+" (%.f)"%(len(filteredLists[variant][0])))
    plt.legend(loc='upper right')
    plt.title('%s\nCorrelation[Position range: %.f-%.f]'%(postfix, posmin, posmax))
    plt.ylim(0, 0.5)
    plt.xlim(0, 400)
    plt.ylabel('Response Frequency')
    plt.xlabel('Epitope Assay Counts')
    pngname = 'plots/Correlation_%s_%s_%s.png'%(posmin, posmax, postfix)
    plt.savefig(pngname.replace('png', 'pdf'), format='pdf')
    plt.savefig(pngname, format='png')
    print ('imgcat %s'%(pngname))
    plt.close()

def main():
    print ("\n\nfile #1: "+inputRF)
    print ("file #2: "+inputEAC+"\n\n")

    inputfileRF = open(inputRF, "r")
    inputfileEAC = open(inputEAC, "r")

    ####### from ResponseFrequency.json #######    
    listRF = []
    listRFPOS = []

    
    while True:
        line = inputfileRF.readline().rstrip()

        if "response frequency" in line:
            rf = line # response frequency
            rf = rf.split()
            rf = rf[-1]
            if ',' in rf: rf = rf[1:-2]
            else: rf = rf[1:-1]
            listRF.append(float(rf))
            #print(rf)
        if "position" in line:
            pos = line # position
            pos = pos.split()
            pos = pos[-1]            
            if ',' in pos: pos = pos.split(',')[0]
            listRFPOS.append(int(pos))
            #print(pos)
                    
        if not line: break 

    #print(listRF)
    #print(listRFPOS)


    ####### from EpitopeAssayCount.json #######    
    listEAC = []
    listEACN = []
    listEACPOS = []

    
    while True:
        line = inputfileEAC.readline().rstrip()

        if "positive" in line:
            eac = line # response frequency
            eac = eac.split()
            eac = eac[-1]            
            if ',' in eac: eac = eac[:-1]
            listEAC.append(float(eac))
            #print(eac)
        if "negative" in line:
            eacn = line # response frequency
            eacn = eacn.split()
            eacn = eacn[-1]            
            if ',' in eacn: eacn = eacn[:-1]
            listEACN.append(float(eacn))
            #print(eac)
        if "position" in line:
            pos = line # position
            pos = pos.split()
            pos = pos[-1]
            if ',' in pos: pos = pos.split(',')[0]
            listEACPOS.append(int(pos))
            #print(pos)
                    
        if not line: break 
    #print(listEAC)
    #print(listEACPOS)

    # if lenth of 4 lits are not the same, exit
    if len(listRF) != len(listRFPOS) or len(listEACPOS) != len(listRFPOS) or len(listEACPOS) != len(listEACPOS):
        print ("lenth of listRF = %.f"%len(listRF))
        print ("lenth of listRFPOS = %.f"%len(listRFPOS))
        print ("lenth of listEAC = %.f"%len(listEAC))
        print ("lenth of listEAC = %.f"%len(listEACPOS)) 
        exit()

    # if listRFPOS and listEACPOS are different, exit
    if listEACPOS != listRFPOS:
        print ("RFPOS and EACPOS are differnet. x-axis should be identical!")
        exit()


    # compute mean and RMS
    mean = np.mean(np.array(listEACN))
    rms = np.sqrt(np.mean(np.square(listEACN)))
    print ("Mean of negative counts is %.2f, RMS=%.2f"%(mean, rms))

    # plot 1D
    plt.figure().set_figwidth(40)
    #plt.plot([1,2,3,4,5,6,7,8,9],[10,11,13,50,0,10,3,4,9]) #
    plt.plot(listRF) #np.array(listRFPOS), np.array(listRF))
    plt.title('Response Frequency')
    plt.ylim(0, 1.0)
    plt.xlabel('Position in Reference Antigen')
    plt.ylabel('Response Frequency')
    pngname = 'plots/ResponseFrequency_vs_Position.png'
    plt.savefig(pngname.replace('png', 'pdf'), format='pdf')
    plt.savefig(pngname, format='png')

    print ('imgcat %s'%(pngname))
    plt.close()

    '''
    # plot 2D
    plt.scatter(listRF, listEAC)
    plt.title('Correlation')
    plt.xlabel('Response Frequency')
    plt.ylabel('Epitope Assay Counts')
    pngname = 'Correlation.png'
    plt.savefig(pngname.replace('png', 'pdf'), format='pdf')
    plt.savefig(pngname, format='png')
    print ('imgcat %s'%(pngname))
    plt.close()
    '''
    drawCorr(listRFPOS[0],listRFPOS[-1], listRF, listEAC)
    drawCorr(listRFPOS[0], 600, listRF, listEAC)
    drawCorr(listRFPOS[0], 300, listRF, listEAC)
    drawCorr(300, 600, listRF, listEAC)
    drawCorr(300, 550, listRF, listEAC)
    drawCorr(300, 530, listRF, listEAC)
    drawCorr(800, 1000, listRF, listEAC)
    drawCorr(601, listRFPOS[-1], listRF, listEAC)

    MaxEACpos = listEAC.index(max(listEAC))+1
    MaxEAC = listRF[listEAC.index(max(listEAC))]
    print ("Maximum EAC is %.2f and its epitope position is %.f"%(MaxEAC, MaxEACpos))

if __name__ == "__main__":
    main()
