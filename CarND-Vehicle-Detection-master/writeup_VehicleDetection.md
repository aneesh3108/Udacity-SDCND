**Vehicle Detection Project**

## [Rubric](https://review.udacity.com/#!/rubrics/513/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

You're reading it!

### Histogram of Oriented Gradients (HOG) & Sliding Window Search

The writeup can be found in the iPython notebook [here](./Walkthrough.ipynb)

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result](./project_video_output.mp4)

Here's a [link to my video result with lane detection](./project_video_output_lane_finding.mp4)

#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

Its recorded in the `Project.ipynb` notebook, but I'll explain it here as well. For videos, there was a need to have previous bounding boxes recorded to ensure smooth transition between frames. As a result, a class `vehicle_detector` was created that took into account the past 10 occurences of the bounding box and then fed those to the `process_frame` function which added the last 10 + current 1 heatmaps and then thresholded overall to get a final output. This ensured that at no point the cars (especially the white car) were lost to the detector and largely diminished the false positives occuring.

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Major key problem: Need more data. I explored the dataset provided in Udacity and figured that the data was more or less imbalanced when it came to identifying vehicles in general. A place where the pipeline will fail is if at all there are trucks on the road, since trucks as an object haven't been represented. It may be a stroke of luck that the SVM has learned that the truck image does not fall under the 'no-car' category and hence classifies it as a car, but I couldn't really verify that. 

Furthermore, the `get_hog_features` consumed a lot of time while training and I'm assuming it eats up a sufficient amount of time during video frames as well and that might be a key problem while trying to achieve good framerates. If I were to implement this in an application, I'd maybe try the C++ implementation to see if its more robust. Furthermore, I would modify the `vehicle_detector` class to not only record the maps, but be initialized with a new object instance every time a car is detected and destroyed once a car is out of frame. This would allow to have individual object tracking, reduce clutter and, ensure that a vehicle that has been detected is not lost till a particular threshold has been met. 

For real time framerates, I'd resort to using deep learning based approaches: tiny - You Only Look Once (YOLO) for instance, which has been known to detect objects robustly. Generally, YOLO frameworks are trained on 20 classes, but since here vehicles is the primary target, I'd probably emphasize that class to utilize YOLO to its max potential and ignore the other classes. 
