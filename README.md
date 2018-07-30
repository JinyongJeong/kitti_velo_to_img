# Velodyne point porject to image (KITTI)

* This code is based on alvinwan's python code (https://github.com/alvinwan/pcp.git). But this code didn't work properly. So I fix code. 

* maintainer: Jinyong Jeong

# How it Works

1. Project point cloud onto the camera, using calibration information.
![scans](https://raw.githubusercontent.com/JinyongJeong/kitti_velo_to_img/master/result/um_000003.jpg)

# Usage

1. Download the KITTI Road [base kit](http://www.cvlibs.net/download.php?file=data_road.zip) and [velodyne](http://www.cvlibs.net/download.php?file=data_road_velodyne.zip).
2. Save `data_road` and `data_road_velodyne` in the root directory of this repository.
3. Run the main script, and then projected image will be save in result forlder. 
