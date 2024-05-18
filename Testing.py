import requests as r
import json
import time
import numpy as np
import threading
import random

url = 'http://172.20.10.1/get?'
what_to_get = ['acc']

start_time = time.time()
data_dict = {}
alreadymoving = False
movementtimes = 0
    
def phyphox_data():
    
    global data_dict
    response = r.get(url + '&'.join(what_to_get)).text
    data = json.loads(response)
    
    # Extract acceleration and gyroscope data
    acc_data = data['buffer'][what_to_get[0]]['buffer'][0]
    
    #apply high pass filter to data
    if acc_data < 0.1:
        acc_data = 0

    print(acc_data)
    return acc_data
    
    print(f'Time: {current_time:.2f}s, Acceleration: {acc_data}')
def fastFourierTransform(time_acc_dict):
    # Extract time and acceleration values from the dictionary
    time_values = np.array(list(time_acc_dict.keys()))
    acceleration_values = np.array(list(time_acc_dict.values()))

    # Compute the FFT of acceleration values
    fft_result = np.fft.fft(acceleration_values)

    # Compute the corresponding frequencies
    dt = time_values[1] - time_values[0]  # Assuming uniform time spacing
    frequencies = np.fft.fftfreq(len(time_values), dt)

    return frequencies, fft_result

# Collect data 100 times with a 1 second interval
for i in range(0, 100):
    if phyphox_data() < 0.1:
        current_time = time.time() - start_time
        data_dict[current_time] = phyphox_data()
        if alreadymoving == True:
            
            alreadymoving = False
    else:
        if alreadymoving == False:
            movementtimes += 1
        
        alreadymoving = True
    
    time.sleep(0.1)
    
returned_frequencies, returned_fft_result = fastFourierTransform(data_dict)

print(returned_frequencies)
print(movementtimes)
print((movementtimes/(time.time() - start_time)))