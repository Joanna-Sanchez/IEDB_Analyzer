#!/usr/bin/env python
import sys, re
import matplotlib.pyplot as plt
import numpy as np

inputRF = sys.argv[1]
inputEAC = sys.argv[2]

def drawCorr(posmin, posmax, listRF, listEAC):
    # plot 2D
    plt.scatter(listEAC[posmin-1:posmax-1], listRF[posmin-1:posmax-1])
    plt.title('Correlation[Position range: %.f-%.f]'%(posmin, posmax))
    plt.ylim(0, 0.5)
    plt.xlim(0, 400)
    plt.ylabel('Response Frequency')
    plt.xlabel('Epitope Assay Counts')
    pngname = 'plots/Correlation_%s_%s.png'%(posmin, posmax)
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
            rf = rf[1:-2]
            listRF.append(float(rf))
            #print(rf)
        if "position" in line:
            pos = line # position
            pos = pos.split()
            pos = pos[-1]            
            listRFPOS.append(int(pos))
            #print(pos)
                    
        if not line: break 

    #print(listRF)
    #print(listRFPOS)


    ####### from EpitopeAssayCount.json #######    
    listEAC = []
    listEACPOS = []

    
    while True:
        line = inputfileEAC.readline().rstrip()

        if "positive" in line:
            eac = line # response frequency
            eac = eac.split()
            eac = eac[-1]
            eac = eac[:-1]
            listEAC.append(float(eac))
            #print(eac)
        if "position" in line:
            pos = line # position
            pos = pos.split()
            pos = pos[-1]            
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

        

    # plot 1D
    plt.figure().set_figwidth(20)
    #plt.plot([1,2,3,4,5,6,7,8,9],[10,11,13,50,0,10,3,4,9]) #
    plt.plot(listRF) #np.array(listRFPOS), np.array(listRF))
    plt.title('Response Frequency')
    plt.xlabel('Position in Reference Antigen')
    plt.ylabel('Response Frequency')
    pngname = 'ResponseFrequency_vs_Position.png'
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
    drawCorr(800, 1100, listRF, listEAC)
    drawCorr(601, listRFPOS[-1], listRF, listEAC)


if __name__ == "__main__":
    main()
