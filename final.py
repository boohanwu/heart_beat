import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal

j = (-1)**0.5
fs = 100
#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)

#z-plot      
angle = np.linspace(-np.pi, np.pi, 50)    
cirx = np.sin(angle)
ciry = np.cos(angle)

z = np.roots([1/6,1/6,1/6,1/6,1/6,1/6])
plt.figure(figsize=(8,8))
plt.plot(cirx, ciry,'k-')
plt.plot(np.real(z), np.imag(z), 'o', markersize=12)

plt.plot(0, 0, 'x', markersize=12)
plt.grid()

plt.xlim((-2, 2))
plt.xlabel('Real')
plt.ylim((-2, 2))
plt.ylabel('Imag')


#initial
fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')


PData= PlotData(500)
ax.set_ylim(-5,5)
ax2.set_ylim(-5,5)
ax3.set_ylim(0,100)
ax3.set_xlim(0,100)
ax4.set_ylim(0,100)
ax4.set_xlim(0,100)

# plot parameters
print ('plotting data...')
# open serial port
strPort='com3'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()

temp = deque(maxlen = 20)

while True:
    #mean = 0
    for ii in range(10):

        try:
            data = float(ser.readline())
            temp.append(data)
            
            PData.add(time.time() - start, data-np.mean(temp))
        except:
            pass
    #mean = np.mean(temp)
    #print(mean)
   
    PData_filter=signal.lfilter([1/6,1/6,1/6,1/6,1/6,1/6], 1, PData.axis_y)    #六點平均濾波器
    xf = np.fft.fft(PData.axis_y)
    xf1 = np.fft.fft(PData_filter)
    w_hat = np.arange(0, fs, fs/len(xf))

    if len(PData_filter)>200:
        p1=0
        p2=80
        for i in range(1,80):
            if PData_filter[i]>PData_filter[p1]:
                p1=i
        for i in range(81,160):
            if PData_filter[i]>PData_filter[p2]:
                p2=i
        HRV = round(((p2-p1)/fs*60),2)
        
        if PData_filter[p1] < 2 or PData_filter[p2] < 2:
            plt.xlabel('HRV: None')
        elif PData_filter[p1] > 50 or PData_filter[p2] > 50:
            plt.xlabel('HRV: None')
        elif HRV > 50 and HRV < 100:
            plt.xlabel('HRV:' + str(HRV))


    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(PData_filter)
    
    #無濾波
    
    line3.set_xdata(w_hat[:len(xf)])
    line3.set_ydata(xf)
    
    #有濾波
    
    line4.set_xdata(w_hat[:len(xf1)])
    line4.set_ydata(xf1)

    fig.canvas.draw()
    fig.canvas.flush_events()
    


    
    
