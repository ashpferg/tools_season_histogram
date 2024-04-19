import numpy as np
from matplotlib import pyplot as plot
import cv2 as cv
import os

def readImage(image_dir, season):

    #Hold the hue/sat values in their own array. 
    hue_array = []
    sat_array = []

    count = 0

    print(season + " start")

    #Read them into the season_img array
    for file in os.listdir(image_dir):

        #Read in every file from given directory
        img = cv.imread(image_dir + file)

        #Switch color mode to Hue/Sat/Value, and split the channels
        #so that we save the hue and sat values separately. "Value" channel discarded.
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h,s,v = cv.split(hsv)

        #Save all the hue values into a single array. Normalize them into range 0-12.
        for i in range(len(h)):
            for j in range(len(h[i])):
                temp = h[i][j]
                temp = round(temp / 180 * 12)
               # temp = round(temp)
                if temp >= 170:
                    temp = 10
                hue_array.append(temp)

        #Save all the sat values into a single array. Normalize them 0-4.
        for i in range(len(s)):
           for j in range(len(s[i])):
               temp2 = s[i][j]
               temp2 = round(temp2 / 256 * 4)
               if temp2 >= 5:
                   temp2 = 4
               sat_array.append(temp2)

        #Console debug: the runtime is slow so you can monitor this to see progress.
        #Runs 0-74 for each season.
        print(count)
        count += 1

    #These are the colors of each bin. Only half are shown on graph due to space.
    color_array = ["red","orange", "yellow", "lime", "green", "turquoise", "teal", "light-blue", "blue", "lavender", "purple", "magenta"]

    #Create a chart that plots hue x sat in bins of 12 x 4.
    fig = plot.figure()
    ax = fig.add_subplot(111,projection='3d')
    hist, x_edge, y_edge= np.histogram2d(hue_array, sat_array, bins=[12,4], range=[[0, 12], [0, 3]])

    xpos, ypos = np.meshgrid(x_edge[:-1] + 1, y_edge[:-1] + 1, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    dx = dy = 1 * np.ones_like(zpos)
    dz = hist.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    #Label each axis. 
    plot.xlabel('Hue: half the bins marked')
    plot.ylabel('Saturation: low to high')
    axis_color_labels = ["red", "", "yellow", "", "green", "", "teal", "", "blue", "", "purple", ""]
    bins = [1,2,3,4,5,6,7,8,9,10,11,12]  

    #Part of my attempt to color the bars - didn't work out.
    plot.xticks(bins, axis_color_labels)

    #Set the graph title and save histogram to [season].jpg
    plot.title(season)
    plot.savefig(season + ".jpg")
    plot.show()

    #View histogram before program closes.
    cv.waitKey()


def main():

    spring_dir = 'images/spring/'
    winter_dir = 'images/winter/'
    summer_dir = 'images/summer/'
    fall_dir = 'images/fall/'

    readImage(spring_dir, "spring")
    readImage(summer_dir, "summer")
    readImage(fall_dir, "fall")
    readImage(winter_dir, "winter")

main()