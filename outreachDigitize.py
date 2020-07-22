folderPath = "/home/kyle/Projects/4Spot/" #include an extra slash at the end

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
dataArr = []
modelArr = []

def readData():
    global dataArr
    global modelArr
    with open(folderPath+"dataFile.csv",'r') as f:
        fullread = list(csv.reader(f))
        dataArr = np.array(fullread[1:],dtype='float64') 
    
    with open(folderPath+"modelFile.csv",'r') as f:
        fullread = list(csv.reader(f))
        modelArr = np.array(fullread[1:],dtype='float64')


try:
    readData()
except:
    print("Need to generate file")
    import sys
    sys.path.insert(1,folderPath)
    import generateDataModels
    readData()
    
#Create Bokeh elements-------------------------------------------------------

dataSrc = ColumnDataSource(data=dict(x=dataArr[:,0],y=dataArr[:,1]))
modelSrc = ColumnDataSource(data=dict(x=modelArr[:,0],y=modelArr[:,1]))

fig = figure(title='Dataset to match', plot_height=300, plot_width=800)

#Default value for figure
fig.line(source=dataSrc, x='x',y='y',color='blue',legend_label='Data')
fig.line(source=modelSrc,x='x',y='y',color='red',legend_label='Model')

dataSelect = Select(title='Dataset:',value='Dataset 1',options=['Dataset 1','Dataset 2'])
modelSelect = Select(title='Model:',value='Sigma of 1',options=['Sigma of 1','Sigma of 0.5'])
xSlider = Slider(start=-5,end=5,value=0,step=0.01,title='Slide model on x axis')
ySlider = Slider(start=0,end=1,value=0,step=0.01,title='Slide model on y axis')
goButton = Button(label='Test results',button_type='success')
results = Paragraph(text="Press the \'Test results\' button see how close you are!")

description = Paragraph(text="The goal of this activity is to try and match a model to a dataset! You can do this by first selecting a dataset you want to test. Then select the type of model you want. Next, move the slider to fit the data as best you can. Finally, select the \'Test Results\' button and it will give you a score. Try to get the highest score on each dataset!")


#Create callback functions for widgets----------------------------------------

def on_dataSelect(attrname, old, new):
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

    

dataSelect.on_change('value', on_dataSelect)
modelSelect.on_change('value', on_modelChange)
xSlider.on_change('value', on_modelChange)
ySlider.on_change('value', on_modelChange)
goButton.on_click(on_goButton)


#Layout of webpage------------------------------------------------------------


layoutList = [[description],[fig],[[dataSelect,modelSelect],[xSlider,ySlider],[goButton,results]]]
l = layout(layoutList,sizing_mode='scale_width')

curdoc().add_root(l)
curdoc().title = "Outreach Activity"
