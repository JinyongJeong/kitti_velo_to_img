# Velodyne point porject to image (KITTI)

* This code is based on alvinwan's python code (https://github.com/alvinwan/pcp.git). But this code didn't work properly. So I fix code. 

* maintainer: Jinyong Jeong

# How it Works

1. Project point cloud onto the camera, using calibration information.
![scans](https://raw.githubusercontent.com/JinyongJeong/kitti_velo_to_img/master/result/um_000003.jpg)

# Usage
1. Make sure your kitti dataset format is like mmdetection3d(https://github.com/open-mmlab/mmdetection3d/blob/master/docs/data_preparation.md)
2. Copy the "data" directory to the root of the repository.
3. Run the main script, and then projected image will be save in result forlder.