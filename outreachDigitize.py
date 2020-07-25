folderPath = "/home/kyle/Projects/4Spot/PatternMatchingGW/" #include an extra slash at the end

#Imports
import numpy as np
import csv
import os

#Bokeh imports
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource
from bokeh.models import Select, Slider, Button, Paragraph
from bokeh.plotting import figure


print("New guest!-------------------")


#Grab data from file---------------------------------------------------------
timeArr = []
easyDataArr = []
mediumDataArr = []
hardDataArr = []

noiseModel = []
monoModel = []
coalModel = []
burstModel = []

def readData():
    global timeArr
    global easyDataArr
    global mediumDataArr
    global hardDataArr

    global noiseModel
    global monoModel
    global coalModel
    global burstModel

    with open(folderPath+"dataFile.csv",'r') as f:
        fullread = list(csv.reader(f))
        header = list(fullread[0])
        dataArr = np.array(fullread[1:],dtype='float64')
        for i in range(len(header)):
            if header[i] == 't':
                timeArr = dataArr[:,i]
            elif header[i] == 'easyData':
                easyDataArr.append(dataArr[:,i])
            elif header[i] == 'mediumData':
                mediumDataArr.append(dataArr[:,i])
            elif header[i] == 'hardData':
                hardDataArr.append(dataArr[:,i])
            else:
                print("Something went wrong... Reading datafile: {}".format(header[i]))
        easyDataArr = np.array(easyDataArr)
        mediumDataArr = np.array(mediumDataArr)
        hardDataArr = np.array(hardDataArr)
        
    
    with open(folderPath+"modelFile.csv",'r') as f:
        fullread = list(csv.reader(f))
        header = list(fullread[0])
        modelArr = np.array(fullread[1:],dtype='float64')
        for i in range(len(header)):
            if header [i] == 't':
                pass
            elif header[i] == 'Noise':
                noiseModel.append(modelArr[:,i])
            elif header[i] == 'Monochromatic':
                monoModel.append(modelArr[:,i])
            elif header[i] == 'Coalescing':
                coalModel.append(modelArr[:,i])
            elif header[i] == 'Burst':
                burstModel.append(modelArr[:,i])
            else:
                print("Something went wrong... Reading modelfile: {}".format(header[i]))
        noiseModel = np.array(noiseModel)
        monoModel = np.array(monoModel)
        coalModel = np.array(coalModel)
        burstModel = np.array(burstModel)


try:
    readData()
except:
    print("Need to generate file")
    import sys
    sys.path.insert(1,folderPath)
    from generateDataModels import generateData
    generateData()
    readData()
    
#Create Bokeh elements-------------------------------------------------------

dataSrc = ColumnDataSource(data=dict(x=timeArr,y=easyDataArr[0]))
modelSrc = ColumnDataSource(data=dict(x=timeArr,y=noiseModel[0]))

fig = figure(title='Dataset to match', plot_height=300, plot_width=800)

#Default value for figure
fig.line(source=dataSrc, x='x',y='y',color='blue',legend_label='Data')
fig.line(source=modelSrc,x='x',y='y',color='red',legend_label='Model')

difficultySelect = Select(title='Select your difficulty:',value='Easy',options=['Easy','Medium','Hard'])
easySelect = Select(title='Choose an Easy dataset:',value='1',options=[str(x) for x in range(1,len(easyDataArr)+1)])
mediumSelect = Select(title='Choose a Medium dataset:',value='1',options=[str(x) for x in range(1,len(mediumDataArr)+1)])
hardSelect = Select(title='Choose a Hard dataset:',value='1',options=[str(x) for x in range(1,len(hardDataArr)+1)])


modelTypeSelect = Select(title='Model Type:',value='Noise',options=['Noise','Monochromatic','Coalescence','Burst'])
noiseSelect = Select(title='Noise model:',value='1',options=['1'])
monoSelect = Select(title='Monochromatic model:',value='1',options=[str(x) for x in range(1,len(monoModel)+1)])
coalSelect = Select(title='Coalescence model:',value='1',options=[str(x) for x in range(1,len(coalModel)+1)])
burstSelect = Select(title='Burst model:',value='1',options=[str(x) for x in range(1,len(burstModel)+1)])

xSlider = Slider(start=-5,end=5,value=0,step=0.01,title='Slide model on x axis (Not functional on Coalescence models)')

goButton = Button(label='Test results',button_type='success')
results = Paragraph(text="Press the \'Test results\' button see how close you are!")

description = Paragraph(text="The goal of this activity is to try and match a model to a dataset! You can do this by first selecting a dataset you want to test. Then select the type of model you want. Next, move the slider to fit the data as best you can. Finally, select the \'Test Results\' button and it will give you a score. Try to get the highest score on each dataset!")


#Create callback functions for widgets----------------------------------------

def on_dataSelect(attrname, old, new):
    diff = difficultySelect.value
    if diff == 'Easy':
        l.children[2].children[0].children[1] = easySelect #Show correct slider
        dataNum = int(easySelect.value)-1
        dataSrc.data=dict(x=timeArr,y=easyDataArr[dataNum])
        
    elif diff == 'Medium':
        l.children[2].children[0].children[1] = mediumSelect #Show correct slider
        dataNum = int(mediumSelect.value)-1
        dataSrc.data=dict(x=timeArr,y=mediumDataArr[dataNum])
        
    else:
        l.children[2].children[0].children[1] = hardSelect #Show correct slider
        dataNum = int(hardSelect.value)-1
        dataSrc.data=dict(x=timeArr,y=hardDataArr[dataNum])
    
    return


def on_modelChange(attrname, old, new):
    modelType = modelTypeSelect.value
    toRoll = int(xSlider.value*100) #If applicable
    if modelType == 'Noise':
        l.children[2].children[1].children[1] = noiseSelect
        modelNum = int(noiseSelect.value)-1
        #no roll
        modelSrc.data = dict(x=timeArr,y=noiseModel[modelNum])
                             
    elif modelType == 'Monochromatic':
        l.children[2].children[1].children[1] = monoSelect
        modelNum = int(monoSelect.value)-1
        #Yes roll
        modelSrc.data = dict(x=timeArr,y=np.roll(monoModel[modelNum],toRoll))
    
    elif modelType == 'Coalescence':
        l.children[2].children[1].children[1] = coalSelect
        modelNum = int(coalSelect.value)-1
        #No roll
        modelSrc.data = dict(x=timeArr,y=coalModel[modelNum])
        
    else:
        l.children[2].children[1].children[1] = burstSelect
        modelNum = int(burstSelect.value)-1
        #Yes roll
        modelSrc.data = dict(x=timeArr,y=np.roll(burstModel[modelNum],toRoll))
    

def on_goButton():
    curData = dataSrc.data['y']
    curModel = modelSrc.data['y']
    res = curData-curModel
    score = int(10000*(1/np.dot(res,res)))
    
    diff = difficultySelect.value
    datasetNum = 0
    if diff == 'Easy':
        datasetNum = easySelect.value
    elif diff == 'Medium':
        datasetNum = mediumSelect.value
        score*=1.5
        score=int(score)
    else:
        score*=2
        score=int(score)
        datasetNum = hardSelect.value
    
    l.children[2].children[2].children[2] = Paragraph(
        text='Your score for {} dataset {} is: {}'.format(diff,datasetNum,score)
    )

    

difficultySelect.on_change('value',on_dataSelect)
easySelect.on_change('value',on_dataSelect)
mediumSelect.on_change('value',on_dataSelect)
hardSelect.on_change('value',on_dataSelect)

modelTypeSelect.on_change('value',on_modelChange)
noiseSelect.on_change('value',on_modelChange)
monoSelect.on_change('value',on_modelChange)
coalSelect.on_change('value',on_modelChange)
burstSelect.on_change('value',on_modelChange)
xSlider.on_change('value',on_modelChange)


goButton.on_click(on_goButton)



#Layout of webpage------------------------------------------------------------


layoutList = [
    [description],
    [fig],
    [[difficultySelect,easySelect],[modelTypeSelect,noiseSelect],[xSlider,goButton, results]]
]
l = layout(layoutList,sizing_mode='scale_width')

curdoc().add_root(l)
curdoc().title = "Outreach Activity"
