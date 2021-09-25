import requests
import pickle
import argparse

class KinectClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_intr(self):
        return pickle.loads(requests.get(f'http://{self.ip}:{self.port}/intr').content)

    def get_camera_data(self, n=1):
        return pickle.loads(requests.get(f'http://{self.ip}:{self.port}/pickle/{n}').content)

if __name__=='__main__':
    parser = argparse.ArgumentParser("Kinect Server")
    parser.add_argument("--ip", type=str, default='0.0.0.0', help="ip")
    parser.add_argument("--port", type=int, default=8080, help="port")
    args = parser.parse_args()

    kinect = KinectClient(args.ip, args.port)
    intr = kinect.get_intr()
    camera_data = kinect.get_camera_data(n=10)
    print(intr)
    print(camera_data['color_img'].shape, camera_data['depth_img'].shape)
