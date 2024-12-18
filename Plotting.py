'''Plotting.py
This script reads the data generated by a 3D lidar sensor and orders each data according to 
its azimuth (rotational angle) & vertical angle, the output of the script is a 3D cloud plotting
alongside a gray scale image od the laser sensings, it saves the grayscale image in a png format.

Authors: Emilio Arredondo Payán (628971) 
Contacts: emilio.arredondop@udem.edu
Organisation: Universidad de Monterrey
First created on Saturday Nobember 25, 2024
'''

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import cv2 




df = pd.read_csv("Complete_data.csv")
df = df.sort_values(['azimuth','Order'],ascending=[True, True])
theta = np.radians(df['azimuth'].to_numpy()/100)
phi = np.radians(df['vert_angle'].to_numpy())
rho = df['distance_m'].to_numpy()*1000
xy = rho*np.cos(phi)
z_coordinate = rho*np.sin(phi)
y_coordinate = xy*np.cos(theta)
x_coordinate = xy*np.sin(theta)




#----------------Image Plotting ---------------------------
image = np.empty((32,0))
for azimuth in df['azimuth'].unique():
    Value = df.loc[df['azimuth']==azimuth]['Color'].to_numpy()
    Value = np.reshape(Value,(32,1))
    image = np.concatenate((image, Value), axis=1)
resized_image = cv2.resize(image.astype(np.uint8), (int(2168/1.1),32*10), interpolation=cv2.INTER_LINEAR)
#-----------------------------------------------------------


#---------------- Plotting ---------------------------------
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x_coordinate,y_coordinate,z_coordinate)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Distances in cm")

plt.show()
cv2.imshow('Ejemplo',resized_image)
cv2.imwrite('Real_size_image.png',image.astype(np.uint8))
cv2.imwrite('resized_image.png',resized_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
#-----------------------------------------------------------