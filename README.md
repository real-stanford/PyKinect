# PyKinect

This is the python package to use Kinect (remotely). It has two parts: server and client.

## Server Installation
- Follow [this guide](https://github.com/microsoft/Azure-Kinect-Sensor-SDK) to install the Azure Kinect SDK (K4A).
- On Ubuntu, you’ll need to set up a udev rule to use the Kinect camera without `sudo`. Follow [these instructions](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md#linux-device-setup).
- Make sure you can run `k4aviewer` from the terminal without `sudo`.
- ```pip install open3d aiohttp imageio```.
- If you are running in ssh, make sure that X11 is running and `export DISPLAY=:0`
- ```python run_server.py --port PORT```
- (optional) Modify `kinect_config.json`. For further instructions, please refer to [this guide](http://www.open3d.org/docs/latest/tutorial/Basic/azure_kinect.html).

## Client Usage
- Option1: browse. Open a browse and visit `IP:PORT/view`. You will see both color image and depth image.
- Option2: python. `KinectClient` can get cam_intr and RGBD image. Please refer to `run_client.py` for more details.