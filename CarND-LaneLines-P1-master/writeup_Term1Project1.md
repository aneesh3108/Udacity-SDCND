# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of the following steps: 

1) Convert the given image in RGB format into grayscale

2) Convert RGB into HSV to extract pixel masks with high yellow and white content

3) Combine the masks with the original image to obtain the final enhanced image that can be given to canny edge detector 

4) Perform Canny edge detection on the enhanced image (that has been slightly blurred with a kernal of 5) 
   Define region of interest - I followed the same trapezoidal region as in the lectures

5) Obtain Hough lines and extrapolate multiple combinations of (x1, y1, x2, y2)s to just 2 of (x1, y1, x2, y2) - for lines at either sides

6) Overlay on original image and obtain output

### 2. Identify potential shortcomings with your current pipeline

1) Straight line fittings don't work accurately when we have curved roads

2) Shadows can cause a major problem - e.g. Challenge video and have to be still dealt with carefully

3) Too much parameter tuning for Canny edge and Hough transform - it will vary from video to video, luckily all 3 videos in this project were in nicely lit conditions (Then again, neural nets have more parameters. No complaints there.) 

4) The current pipeline will probably fail when it comes to poorly lit or evening/night time conditions - that will require extra set of adjustments that the current pipeline doesn't have. 

5) What about places where the lanes aren't marked properly? More over, double line markings on either side of the roads. 

### 3. Suggest possible improvements to your pipeline

1) Incorporate temporal changes into the pipeline - especially in videos, line locations in previous frame can be used for predicting line location in next frame and prevent haphazard transformations which where observed before finetuning parameters. 

2) Use regression techniques instead of slope checkings to find optimal lines. May prevent a lot of 'divide-by-zero' errors that occured. 
