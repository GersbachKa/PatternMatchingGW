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
easySelect = Select(title='Choose a dataset:',value='1',options=[str(x) for x in range(1,len(easyDataArr)+1)])
mediumSelect = Select(title='Choose a dataset:',value='1',options=[str(x) for x in range(1,len(mediumDataArr)+1)])
hardSelect = Select(title='Choose a dataset:',value='1',options=[str(x) for x in range(1,len(hardDataArr)+1)])


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
        modelNum = int(easySelect.value)-1
        dataSrc.data=dict(x=timeArr,y=easyDataArr[modelNum])
        
    elif diff == 'Medium':
        l.children[2].children[0].children[1] = mediumSelect #Show correct slider
        modelNum = int(mediumSelect.value)-1
        dataSrc.data=dict(x=timeArr,y=mediumDataArr[modelNum])
        
    else:
        l.children[2].children[0].children[1] = hardSelect #Show correct slider
        modelNum = int(hardSelect.value)-1
        dataSrc.data=dict(x=timeArr,y=hardDataArr[modelNum])
    
    return
    
    value = dataSelect.value
    if value == 'Dataset 1':
        dataSrc.data=dict(x=dataArr[:,0],y=dataArr[:,1])
    elif value == 'Dataset 2':
        dataSrc.data=dict(x=dataArr[:,2],y=dataArr[:,3])
    else:
        print("Something went wrong... (data select)")

def on_modelChange(attrname, old, new):
    modelVal = modelSelect.value
    toRoll = int(xSlider.value*100)
    toAdd = ySlider.value
    if modelVal =='Sigma of 1':
        modelSrc.data=dict(x=modelArr[:,0],y=np.roll(modelArr[:,1],toRoll)+toAdd)
    elif modelVal =='Sigma of 0.5':
        modelSrc.data=dict(x=modelArr[:,2],y=np.roll(modelArr[:,3],toRoll)+toAdd)
    else:
        print("Something went wrong... (model select)")


def on_goButton():
    curData = dataSrc.data['y']
    curModel = modelSrc.data['y']
    res = curData-curModel
    score = int(10000*(1/np.dot(res,res)))
    l.children[2].children[2].children[1] = Paragraph(text='Your score for {} is: {}'.format(dataSelect.value,score))

    

difficultySelect.on_change('value',on_dataSelect)

#Layout of webpage------------------------------------------------------------


layoutList = [
    [description],
    [fig],
    [[difficultySelect,easySelect],[modelTypeSelect,noiseSelect],[xSlider,[goButton, results]]]
]
l = layout(layoutList,sizing_mode='scale_width')

curdoc().add_root(l)
curdoc().title = "Outreach Activity"
