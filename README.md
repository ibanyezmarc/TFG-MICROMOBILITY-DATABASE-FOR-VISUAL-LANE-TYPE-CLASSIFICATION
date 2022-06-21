# MICROMOBILITY DATABASE FOR VISUAL LANE TYPE CLASSIFICATION

The use and development of micromobility solutions and vehicles in cities is growing too fast, causing possible dangers due to the circulation of different users. In this project we create a proper video database suitable for a project  based on a Deep Learning model that detects different types of lanes, being able to improve  both drivers and pedestrian security.

A camera is attached to a VMP, facing forward in the direction of the ride. The video feed from this camera is used to
determine the type of lane the VMP is circulating on. For this, we use both frame-to-frame and video-based classifiers.

- model_testing/  
  Trained models and its scripts to test them.
  
- preprocessing/  
  Scripts to preprocess videos: downsample, extract frames, generate index files with GNSS data, etc.
