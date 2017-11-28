#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:34:49 2017

@author: aneesh
"""

import os, cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import imread, imresize
from scipy.stats import bernoulli
from sklearn.utils import shuffle

# steering constant to balance left and right images (between 0.2 - 0.3)
STEERING_CONST = 0.25 

def load_data(img_path = 'data/', csv_path = 'data/driving_log.csv'):

    data = pd.read_csv(csv_path)
    
    imgs_path = []
    angles = []
    for idx in range(data.shape[0]):
        # strip() is used since some paths in the CSV have space and cause an error
        imgs_path.append(os.path.join(img_path, data.center[idx].strip()))
        angles.append(float(data.steering[idx]))        
        
        imgs_path.append(os.path.join(img_path, data.left[idx].strip()))
        angles.append(float(data.steering[idx]) + STEERING_CONST)
    
        imgs_path.append(os.path.join(img_path, data.right[idx].strip()))
        angles.append(float(data.steering[idx]) - STEERING_CONST)
    
    return imgs_path, angles

# Data balancing as per notes from https://github.com/jeremy-shannon/CarND-Behavioral-Cloning-Project
def balance_data(imgs_path, angles, nbins = 25, show = False):
    hist, bins = np.histogram(angles, nbins)
    avg_samples = len(angles)/ nbins

    if show:
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.plot((np.min(angles), np.max(angles)), (avg_samples, avg_samples), 'k-')
        
    keep_probs = []
    target = avg_samples * .5
    for i in range(nbins):
        if hist[i] < target:
            keep_probs.append(1.)
        else:
            keep_probs.append(1./(hist[i]/target))
    remove_list = []
    for i in range(len(angles)):
        for j in range(nbins):
            if angles[i] > bins[j] and angles[i] <= bins[j+1]:
                # delete from X and y with probability 1 - keep_probs[j]
                if np.random.rand() > keep_probs[j]:
                    remove_list.append(i)
    imgs_path = np.delete(imgs_path, remove_list, axis=0)
    angles = np.delete(angles, remove_list)
    if show:
        hist, bins = np.histogram(angles, nbins)
        plt.bar(center, hist, align='center', width=width)
        plt.plot((np.min(angles), np.max(angles)), (avg_samples, avg_samples), 'k-')
    
    return imgs_path, angles
    
# removes the sky since it is not favorable and resizes the image to 66 x 200 x 3 
def img_preproc(img):
    new_img = img[50:140,:,:]
    new_img = cv2.GaussianBlur(new_img, (3,3), 0)
    new_img = imresize(new_img, (66,200))
    new_img = cv2.cvtColor(new_img, cv2.COLOR_RGB2YUV)
    return new_img

# image flip + steering angle inverted
def img_flip(img, angle):
    return np.fliplr(img), -1 * angle

# https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
def img_gamma(img):
    gamma = np.random.uniform(0.2, 1.0)
    invGamma = 1.0/ gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

# random brightness adjustment to tackle shadows
def img_bright(image):
    image1 = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
    random_bright = 0.8 + 0.4*(2*np.random.uniform()-1.0)    
    image1[:,:,2] = image1[:,:,2]*random_bright
    image1 = cv2.cvtColor(image1,cv2.COLOR_HSV2RGB)
    return image1

# data generator for Keras
def gen_data(imgs_path, angles, batch_size = 64, train_flag = True):
    imgs_path, angles = shuffle(imgs_path, angles)
    col_img = []
    col_angles = []
    while True: 
        for i in range(len(angles)):
            img = imread(imgs_path[i])
            angle = angles[i]
          
            if train_flag and np.random.rand() < 0.6:
                img, angle = img_flip(img, angle)
            
            if train_flag and bernoulli.rvs(0.5):
                img = img_gamma(img)
            else:
                img = img_bright(img)
            
            img = img_preproc(img)
            col_img.append(img)
            col_angles.append(angle)
            if len(col_img) == batch_size:
                yield(np.array(col_img), np.array(col_angles))
                col_img, col_angles = ([], [])
        imgs_path, angles = shuffle(imgs_path, angles)