import json
import time

import numpy as np
import open3d
import os


def get_intr(config, device, align_depth_to_color, record_filename, intr_json_filename):
    # get intrinsic
    recorder = open3d.io.AzureKinectRecorder(config, device)
    recorder.init_sensor()
    recorder.open_record(record_filename)
    recorder.record_frame(True, align_depth_to_color)
    recorder.close_record()
    reader = open3d.io.AzureKinectMKVReader()
    reader.open(record_filename)
    metadata = reader.get_metadata()
    open3d.io.write_azure_kinect_mkv_metadata(intr_json_filename, metadata)


class Kinect(object):
    def __init__(self, device, config=None, align_depth_to_color=True, depth_scale_offset=None):
        if config is not None:
            config = open3d.io.read_azure_kinect_sensor_config(config)
        else:
            print('[Warning] No Kinect Config!')
            config = open3d.io.AzureKinectSensorConfig()
        self.align_depth_to_color = align_depth_to_color

        # get intr
        record_filename = 'intr_record.mkv'
        intr_json_filename = 'intrinsic.json'
        get_intr(config, device, self.align_depth_to_color, record_filename, intr_json_filename)
        self.color_intr = np.array(json.load(open('intrinsic.json'))['intrinsic_matrix']).reshape([3, 3]).T
        os.remove(record_filename)
        os.remove(intr_json_filename)
        
        self.sensor = open3d.io.AzureKinectSensor(config)
        if not self.sensor.connect(device):
            raise RuntimeError('Failed to connect to sensor')
        self.depth_scale_offset = 1 if depth_scale_offset is None else np.loadtxt(depth_scale_offset)
        
    
    def get_rgbd(self):
        while True:
            rgbd = self.sensor.capture_frame(self.align_depth_to_color)
            if rgbd is None:
                continue
            color_img = np.asarray(rgbd.color)
            depth_img = np.asarray(rgbd.depth).astype(np.float) / 1000.
            return color_img, depth_img


    def get_avg_depth(self, n, imsize):
        self.max_depth = 5
        ds = np.empty((imsize[0], imsize[1], n), dtype=np.float64)
        for i in range(n):
            _, depth_img = self.get_rgbd()
            ds[:, :, i] = depth_img
            time.sleep(0.001)
        ds[ds == 0] = np.nan
        d = np.nanmedian(ds, axis=2)
        d[np.isnan(d)] = self.max_depth
        d[d == 0] = self.max_depth
        d[d > self.max_depth] = self.max_depth
        return d

    def get_camera_data(self, n=50):
        color_img, depth_img = self.get_rgbd()
        if n > 1:
            depth_img = self.get_avg_depth(n, color_img.shape)
        depth_img *= self.depth_scale_offset
        return color_img, depth_img
