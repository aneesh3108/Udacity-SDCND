## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Writeup / README

You're on the page right now. 

### Pipeline (single images)

The writeup can be found in the iPython notebook [here](./Walkthrough.ipynb)

Here's a [link to my video result](./project_video_output.mp4) 

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

The problems I encountered were almost exclusively due to lighting conditions, shadows, discoloration, etc: most of the 14 hour timeperiod was spent on finding the right set of thresholds for the binary image. It was finally adjusted to not include the edge map at all since color based thresholds worked well overall. I thought the pipeline would fail in the evening/night conditions when there is lack of brightness, however I believe adaptive color thresholds would take care that. To make it more robust, I would possibly have to make it more workable for conditions under snow, rain and fog - something that neither of the provided videos contain.  
