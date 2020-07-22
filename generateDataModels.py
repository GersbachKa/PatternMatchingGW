folderPath = "/home/kyle/Projects/4Spot/" #include an extra slash at the end

import numpy as np
import csv

def norm(x,mu=0,sigma=1):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp((-1/2)*(((x-mu)/sigma)**2))


data1x = np.linspace(-5,5,1000)
data1y = [norm(x,-1.32,0.5)+np.random.normal(0,.05)+0.44 for x in data1x]

data2x = np.linspace(-5,5,1000)
data2y = [norm(x,2.56,1)+np.random.normal(0,.05)+0.39 for x in data2x]


model1x = np.linspace(-5,5,1000)
model1y = np.array([norm(x) for x in model1x])

model2x = np.linspace(-5,5,1000)
model2y = np.array([norm(x,sigma=0.5) for x in model2x])


with open("dataFile.csv",'w') as f:
    write=csv.writer(f)
    write.writerow(['Data1_x','Data1_y','Data2_x','Data2_y'])
    
    for i in range(0,len(data1x)):
        write.writerow([data1x[i],data1y[i],data2x[i],data2y[i]])
    
with open("modelFile.csv",'w') as f:
    write=csv.writer(f)
    write.writerow(['Model1_x','Model1_y','Model2_x','Model2_y'])
    
    for i in range(0,len(model1x)):
        write.writerow([model1x[i],model1y[i],model2x[i],model2y[i]])

