import argparse
import pickle
from io import BytesIO

import imageio
import numpy as np
from aiohttp import web

import pyk4a
from pyk4a import Config, PyK4A

# launch kinect
k4a = PyK4A(
    Config(
        camera_fps=pyk4a.FPS.FPS_30,
        color_resolution=pyk4a.ColorResolution.RES_720P,
        depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
    )
)
k4a.start()

# set exposure parameters
k4a.exposure_mode_auto = False
k4a.exposure = 8330

async def view_handle(request):
    img_buf = BytesIO()
    capture = k4a.get_capture()
    color_img = capture.color
    depth_img = capture.transformed_depth

    color_img = color_img[...,[2,1,0]].astype(np.float32) / 255.0
    depth_img = depth_img.astype(np.float32)

    depth_img -= np.min(depth_img)
    depth_img /= np.max(depth_img)
    img = np.concatenate([color_img, np.repeat(depth_img[:, :, np.newaxis], 3, axis=2)], axis=0)
    imageio.imwrite(img_buf, (img * 255).astype(np.uint8), format='jpeg')

    return web.Response(body=img_buf.getbuffer(), content_type='image/jpeg')


async def pickle_handle(request):
    img_buf = BytesIO()
    capture = k4a.get_capture()
    color_img = capture.color
    depth_img = capture.transformed_depth
    color_img = color_img[...,[2,1,0]]

    enc = pickle.dumps({
        'color_img':color_img,
        'depth_img':depth_img
    })
    return web.Response(body=enc)


async def intr_handle(request):
    color_intr = k4a.calibration.get_camera_matrix(pyk4a.calibration.CalibrationType.COLOR)
    enc = pickle.dumps(color_intr)
    return web.Response(body=enc)


app = web.Application()
app.add_routes([web.get('/', view_handle),
                web.get('/view', view_handle),
                web.get('/intr', intr_handle),
                web.get('/pickle', pickle_handle)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Kinect Server")
    parser.add_argument("--port", type=int, default=8080, help="port")
    args = parser.parse_args()

    web.run_app(app, port=args.port)
