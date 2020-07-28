folderPath = "gravitySleuth/" #include an extra slash at the end

import numpy as np
import csv
import random

start = 0
stop = 10
datapoints = 10000
dt = (stop-start)/datapoints

#Functions for generating data-------------------------------------------
def burst(t,mu,sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp((-1/2)*(((t-mu)/sigma)**2))

def monochromatic(t,amplitude,period,phase):
    phase = 0
    return amplitude*np.cos(((2*np.pi*t)/period + phase))

def coalescing(t,A,B,t_c,phi_c,lamb):
    if t<t_c:
        return A*(B*(t_c-t))**(-1/4)*np.cos(2*phi_c-(B*(t_c-t))**(5/8))
    else:
        temp = A*(B*(dt))**(-1/4)*np.cos(2*phi_c-(B*(dt))**(5/8))
        temp*=np.exp((t_c-dt)/lamb)*np.exp(-(t/lamb))
        return temp

def wNoise(sigma):
    return np.random.normal(0,sigma)


#Functions to create data and write it to file------------------------------

def generateData():
    datasetT = list(np.linspace(0,10,1000))
   
    easyData = []
    mediumData = []
    hardData = []
    
    #MONOCHROMATIC---------------------------
    #4 monoChromatic datasets : ALL DATASETS HAVE A=0.5
    
    #Easy waveform: T=5
    easyData.append([monochromatic(t,0.5,5,(np.pi/2))+wNoise(.25) for t in datasetT])

    #Medium waveform: T=4
    mediumData.append([monochromatic(t,0.5,4,0)+wNoise(.4) for t in datasetT])

    #Hard waveform: T=3
    hardData.append([monochromatic(t,0.5,3,np.pi)+wNoise(.75) for t in datasetT])

    #Hard: T= 10
    hardData.append([monochromatic(t,0.5,10,np.pi)+wNoise(.75) for t in datasetT])

    #9 monochromatic models: A=0.5, T:(1:10)
    monoModels = []
    for i in range(1,11):
        monoModels.append([monochromatic(t,0.5,i,0) for t in datasetT])

    
    #COALESCING-----------------------------

    #Easy coalescence
    easyData.append([coalescing(t,200,80,6,np.pi/4,0.1)/100+wNoise(.2) for t in datasetT])

    #medium coalescence
    mediumData.append([coalescing(t,200,40,9,np.pi/4,0.1)/100+wNoise(.3) for t in datasetT])

    #Hard coalescence
    hardData.append([coalescing(t,10,10,9,np.pi/4,0.1)/5+wNoise(.7) for t in datasetT])


    #6 Coalescent models
    coalModels = []
    coalModels.append([coalescing(t,10,500,6,np.pi/4,0.1)/4 for t in datasetT])
    coalModels.append([coalescing(t,1,5,6,np.pi/4,0.1)*1.5 for t in datasetT])
    coalModels.append([coalescing(t,200,80,6,np.pi/4,0.1)/100 for t in datasetT])
    coalModels.append([coalescing(t,10,500,9,np.pi/4,0.1)/4 for t in datasetT])
    coalModels.append([coalescing(t,1,5,9,np.pi/4,0.1)*1.5 for t in datasetT])
    coalModels.append([coalescing(t,200,40,9,np.pi/4,0.1)/100 for t in datasetT])
    coalModels.append([coalescing(t,10,10,9,np.pi/4,0.1)/5 for t in datasetT])


    #BURSTS----------------------------------

    #Easy burst
    easyData.append([burst(t,6,.8)+wNoise(.08) for t in datasetT])
    
    #Medium burst
    mediumData.append([-burst(t,7,1)+wNoise(.14) for t in datasetT])
    
    #Hard burst
    hardData.append([-burst(t,5,1.4)+wNoise(.18) for t in datasetT])
    
    #Hard burst
    hardData.append([burst(t,6,1.4)+wNoise(.2) for t in datasetT])
        
    
    #burst models
    burstModels = []
    #Positive bursts
    burstModels.append([burst(t,5,.6) for t in datasetT])
    burstModels.append([burst(t,5,.8) for t in datasetT])
    burstModels.append([burst(t,5,1) for t in datasetT])
    burstModels.append([burst(t,5,1.2) for t in datasetT])
    burstModels.append([burst(t,5,1.4) for t in datasetT])
    #Negative bursts
    burstModels.append([-burst(t,5,.6) for t in datasetT])
    burstModels.append([-burst(t,5,.8) for t in datasetT])
    burstModels.append([-burst(t,5,1) for t in datasetT])
    burstModels.append([-burst(t,5,1.2) for t in datasetT])
    burstModels.append([-burst(t,5,1.4) for t in datasetT])
    
    #NOISE-----------------------------------
    
    hardData.append([wNoise(.1) for t in datasetT])
    hardData.append([wNoise(.2) for t in datasetT])
    mediumData.append([wNoise(.2) for t in datasetT])
    mediumData.append([wNoise(.4) for t in datasetT])
    easyData.append([wNoise(.5) for t in datasetT])
    
    noiseModel = [0 for t in datasetT]
    
    #Randomize datasets
    random.shuffle(easyData)
    random.shuffle(mediumData)
    random.shuffle(hardData)
    
    writeData(datasetT,easyData,mediumData,hardData,
              noiseModel,monoModels,coalModels,burstModels)
    
    
    
def writeData(timeList,eData,mData,hData,nMod,mMod,cMod,bMod):
    
    with open(folderPath+"Datafiles/dataFile.csv",'w') as f:
        write=csv.writer(f)
        titleColumn = ['t']
        titleColumn.extend(['easyData']*len(eData))
        titleColumn.extend(['mediumData']*len(mData))
        titleColumn.extend(['hardData']*len(hData))
        write.writerow(titleColumn)
    
        for timestep in range(len(timeList)):
            row = [timeList[timestep]]
            for dataset in range(len(eData)):
                row.append(eData[dataset][timestep])
            for dataset in range(len(mData)):
                row.append(mData[dataset][timestep])
            for dataset in range(len(hData)):
                row.append(hData[dataset][timestep])
                
            write.writerow(row)
            
    
    with open(folderPath+"Datafiles/modelFile.csv",'w') as f:
        write=csv.writer(f)
        titleColumn = ['t']
        titleColumn.extend(['Noise'])
        titleColumn.extend(['Monochromatic']*len(mMod))
        titleColumn.extend(['Coalescing']*len(cMod))
        titleColumn.extend(['Burst']*len(bMod))
        write.writerow(titleColumn)
    
        for timestep in range(len(timeList)):
            row = [timeList[timestep],nMod[timestep]]
            for model in range(len(mMod)):
                row.append(mMod[model][timestep])
            for model in range(len(cMod)):
                row.append(cMod[model][timestep])
            for model in range(len(bMod)):
                row.append(bMod[model][timestep])
                
            write.writerow(row)

