# Image Stitching and Search Application

## Introduction
To register images together, one needs to follow certain steps to acquire useful information to be able to stitch images together. The first step in image registration is to find and extract the best and most robust features. It is the feature extraction that determines the image registration computational complexity and accuracy. The most representative features are points, curves, and contours [yu2014][ liu2010][li2008]. Image feature point extraction algorithm includes SUSAN, Harris, SIFT, etc. Scale Invariant Feature Transform (SIFT) is one of the most powerful approaches to find matching points between images [wang2008]. SIFT is shown to be robust against rotation and scaling which proves its various applications in image processing. 
SIFT Algorithm for Image Registration
Without going into much detain, SIFT can be implemented in the following steps [moreno2009, lin2012 and references herein]:

Constructing a scale space Create internal representations of the original image to ensure scale invariance. This is done by generating a “scale space”.
	DoG Approximation The Difference of Gaussian for finding key points in an image.
	Finding key-points  Key points are maxima and minima in the Difference of Gaussian image.
	Removing of bad key points  Removing edges and low contrast regions. Eliminating these makes the algorithm efficient and robust.
	Assigning an orientation to the key-points This cancels out the effect of orientation, making it rotation invariant.
	Generate SIFT features Finally, with scale and rotation invariance in place, one more representation is generated. This helps uniquely identify features.
  
### Finding Matched Between Two Images
In order to stitch two or more images together, one needs to find the similar invariant features or key point in each image. After calculating the feature points for each image using SIFT, a brute-force matcher can be used (with K-nearest neighbor approach) to find the matches between two images.
Homography Matrix
In order to calculate a homography matrix for two images, a reasonably good set of common key point must be chosen. It has been shown in the literature that RAndom SAmple Consensus (RANSAC) is a robust method to be used for calculating the homography matrix [fischler1981]. A simple explanation of how this method can be implemented can be found below [derpanis2010]: 

	RANSAC loop: 
	Select four feature pairs (at random)
	Compute homography matrix H (the exact representation) 
	Compute inliers
	Keep largest set of inliers Re-compute least-squares H estimate using all inliers   

### Implementation Details of Image Stitching
Most of the approached that uses SIFT and RANSAC to come of with a solution for image registration use extra information, such as the order of the images and number of them. The provided code alongside of this report is an effort to remove this restriction so that any set of images with reasonable overlapping can be used to create a larger image. In writing the code, OpenCV documentation and [rose2016] are used extensively.

### Object detection and Classification
The second part of the project is related to object detection and classification of the final image. However deep learning approaches such as single shot detector (SSD) [liu2015] are shown to have superior performance in detecting multiple objects, given a specific scenario like images with front faces, back of the books, etc. which have robust features can be detected using histogram of gradient (HOG) feature and multiscale deformable part models [felzenszwalb2010], Haar feature detection [lienhart2002][ mita2005] , etc.
Here a simple Haar cascade face detection models are used to detected the faces in the final stitched image. For objects that do not have rotational features like a car in different poses, Haar cascade models prove to be good for multiple object detection of a specific class. As the final step in this project, the detected objects (faces for instance) were compared with a library of images to find the matches. If a match exists, then one can fetch specific information regarding that object and shows it to the user.

### Conclusion and Remarks
In this project, a robust image stitching algorithm along with an object detector and library search is presented as explained in the assignment. Smaller pieces of the project are inherited from open sourced documentations and/or libraries but not consultation is received from other individuals.
 
## References
[wang2008] Wang, Xiaohua and Fu, Weiping, “Optimized SIFT image matching algorithm”, IEEE International Conference on Automation and Logistics, ICAL, (2008), pp. 843-847.

[yu2014] L. Yu and J. Xie, “A Remote Sensing Image Classification Method Combining Multiple Features”, Computer Application and Software, vol. 31, no. 11, (2014), pp. 183-185. 

[liu2010] Z. Liu and J. Chu, “Feature Extraction and Template Matching Combined with Image Stitching Method”, Micro-Computer Information, vol. 26, no. 1, (2010), pp. 117-118. 

[li2008] D. Li and Y. Wang, “Research of the Image Mosaic Method Based on Corner Match”, Chinese Journal of Electron Devices, vol. 31, no. 3, (2008), pp. 919-922.

[moreno2009] Plinio Moreno, Alexandre Bernardino, and José Santos Victor, "Improving the SIFT descriptor with smooth derivative filters," Pattern Recognition Letters, vol. Volume 30, no. 1, (2009), pp. 18-26. 

[lin2012] D.T. Lin and C. H. Hsu, "Improving the Efficiency and Accuracy of SIFT Image Matching", Proceedings of the 2nd International Congress on Computer Applications and Computational Science, vol. 145, F. L. Gaol and Q. V. Nguyen, Eds., Springer Berlin Heidelberg, (2012), pp. 227-233.

[fischler1981] M. A. Fischler, R. C. Bolles. “Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis and Automated Cartography”. Comm. of the ACM, Vol 24, (1981), pp 381-395.

[derpanis2010] Derpanis KG, Overview of the RANSAC algorithm. Technical report, Computer Science, York University, 2010.

[rose2016] A. Rosebrock, Practical Python and OpenCV, pyimagesearch Publications, Miami, 2016.

[liu2015] W. Liu, D. Anguelov, D. Erhan, C. Szegedy, and S. Reed, “SSD: Single shot multibox detector,” arXiv:1512.02325, 2015.

[felzenszwalb2010] P. Felzenszwalb, R. Girshick, D. McAllester, and D. Ramanan. Object detection with discriminatively trained part based models. TPAMI, 2010.

[lienhart2002] R. Lienhart and J. Maydt. An extended set of Haar-like features for rapid object detection. In Proc. of the International Conference on Image Processing (ICIP), pages 900–903, 2002.

[mita2005] T. Mita, T. Kaneko, and O. Hori. Joint Haar-like features for face detection. In Proc. of ICCV, 2005

