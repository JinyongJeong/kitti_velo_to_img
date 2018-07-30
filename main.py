"""Label point clouds using image 2d annotation and calibration files."""

from thirdparty.calib import Calib

import argparse
import os
import cv2
import numpy as np
import sys


def main():
    parser = argparse.ArgumentParser(description='Converter')
    parser.add_argument('--kitti-road', type=str, help='Path to KITTI `data_road`', default='data_road/')
    parser.add_argument('--kitti-road-velodyne', type=str, help='Path to KITTI `data_road_velodyne`', default='data_road_velodyne/')
    parser.add_argument('--cam-idx', type=int, help='Index of the camera being used', default=2)
    parser.add_argument('--dataset', type=str, choices=('training', 'testing'), help='Which dataset to run on', default='training')
    args = parser.parse_args()

    dirpath = os.path.join(args.kitti_road_velodyne, args.dataset, 'velodyne')

    for filename in os.listdir(dirpath):
        if filename.startswith('.'):
            continue
        name = filename.split('.')[0] 
        prefix = name.split('_')[0] #um umm uu
        id = name.split('_')[1]
        velo_path = os.path.join(args.kitti_road_velodyne, args.dataset, 'velodyne', filename)
        calib_path = os.path.join(args.kitti_road, args.dataset, 'calib', '%s.txt' % name)
        gt_path = os.path.join(args.kitti_road, args.dataset, 'gt_image_2', '%s_road_%s.png' %(prefix ,id))
        img_path = os.path.join(args.kitti_road, args.dataset, 'image_2', '%s.png' % name)

        # n x 4 (x, y, z, intensity)
        velo_raw_data = np.fromfile(velo_path, dtype=np.float32).reshape((-1, 4))
        velo_raw_points = velo_raw_data[:, :3]

        #filtering velodyne point (only front point)
        x, y, z = velo_raw_points.T
        selector1 = (x > 0)
        velo_points = velo_raw_points[selector1]
        velo_data = velo_raw_data[selector1]

        gt = cv2.imread(gt_path, cv2.IMREAD_UNCHANGED)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if gt is None:
            print('\r%s does not have a ground truth file' % filename)
            continue
        gt_labels = gt[:, :, 0]
        h, w = gt_labels.shape

        calib = Calib(calib_path)

        img_points = calib.velo2img(velo_points, args.cam_idx).astype(int)

        x, y = img_points.T
        selector2 = (y < h) * (y > 0) * (x < w) * (x > 0)
        filtered_img_points = img_points[selector2]
        velo_new_data = velo_data[selector2]

#        y, x = np.round(filtered_img_points).astype(int).T
#        velo_labels = gt_labels[y, x].reshape(y.shape[0], 1)

        for point in filtered_img_points:
            img[point[1],point[0]] = (0,255,255)

        save_name = os.path.join('result','%s.jpg' % name)
        cv2.imwrite(save_name, img)


        # Uncomment to visualize portion of LIDAR scan labeled "drivable"
        # img = np.zeros(gt.shape)
        # for x, y, label in zip(x, y, velo_labels):
        #     img[y, x] = label
        # cv2.imwrite('drivable.jpg', img)

        # n x 4 (x, y, z, intensity, drivable) - excludes anything not in cam
        #velo_new_data = np.hstack((velo_new_data, velo_labels))
        #velo_new_path = os.path.join(args.kitti_road_velodyne, args.dataset, 'gt_velodyne', name)
        #os.makedirs(os.path.dirname(velo_new_path), exist_ok=True)
        #np.save(velo_new_path, velo_new_data)
        #sys.stdout.write("\rConverted %s" % filename)
        #sys.stdout.flush()

    print('Done')

if __name__ == '__main__':
    main()
