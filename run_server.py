import argparse
import pickle
from io import BytesIO

import imageio
import numpy as np
from aiohttp import web

from cameras import Kinect

camera = Kinect(
    device=0,
    align_depth_to_color=True,
    config='kinect_config.json',
    depth_scale_offset=None
)

async def view_handle(request):
    img_buf = BytesIO()
    color_img, depth_img = camera.get_camera_data(n=1)
    color_img = color_img / 255.0

    depth_img -= np.min(depth_img)
    depth_img /= np.max(depth_img)
    img = np.concatenate([color_img, np.repeat(depth_img[:, :, np.newaxis], 3, axis=2)], axis=0)
    imageio.imwrite(img_buf, img, format='jpeg')

    return web.Response(body=img_buf.getbuffer(), content_type='image/jpeg')


async def pickle_handle(request):
    n = int(request.match_info.get('avg', 1))
    print(n)
    img_buf = BytesIO()
    color_img, depth_img = camera.get_camera_data(n=n)
    cam_intr = camera.color_intr

    enc = pickle.dumps({
        'color_img':color_img,
        'depth_img':depth_img
    })
    return web.Response(body=enc)


async def intr_handle(request):
    enc = pickle.dumps(camera.color_intr)
    return web.Response(body=enc)


app = web.Application()
app.add_routes([web.get('/', view_handle),
                web.get('/view', view_handle),
                web.get('/intr', intr_handle),
                web.get('/pickle', pickle_handle),
                web.get('/pickle/{avg}', pickle_handle)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Kinect Server")
    parser.add_argument("--port", type=int, default=8080, help="port")
    args = parser.parse_args()

    web.run_app(app, port=args.port)
