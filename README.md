# SWIT-Dataset
## Introduction

Scaffolding Worker IMU Time-series (SWIT) Dataset for Deep Learning-based Construction Site Behavior Recognition

## Unsafe Behavior Categories
* 4 behaviors are related to hazardous construction environments (Obstacle; Slip; Hole; Unstable)
* 2 behaviors are related to worker-compliance (Climb; Step-off)
* 2 behaviors are related to musculoskeletal risk postures (Squat; Kneel)
* 1 behavior is related to emergency situations (Fall-down)
* 1 behavior is related to general situations (Walk)   [involved walking forward, walking sideways, walking backward, briefly stopping, and working in a safe manner]
![Visual Example for each behavioral category](https://github.com/user-attachments/assets/4d1632c3-31b7-4b73-9459-5b3093770b50)

## Experimental Setup for dataset acquisition
* Participants: 27 construction engineering expert
* IMU Sensor: EBIMU24GV5 wireless IMU sensor, 100Hz sampling rate
* Sensor placement: Attached to the lower back of participants
* Camera: GoPro Hero 12 black, recording at 25 FPS
* Data collection method: Each participant repeated 10 behaviors 10 times each
* Data synchronization: Time synchronization between IMU sensor data and video data
* Pose estimation: 17 keypoints extracted from video using YOLOv7-pose
![Experimental Setup](https://github.com/user-attachments/assets/bced9bc7-c47d-496d-8d36-516e1215c9c1)
## Download the SWIT-Dataset
* It will be appeared soon
