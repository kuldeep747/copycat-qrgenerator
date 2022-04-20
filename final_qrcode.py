from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os
import pyqrcode
import time
app = Flask(__name__)


@app.route("/", methods=['GET'])
def display():
    url = pyqrcode.create(request.args['uId'])
    url.png("display.png", scale=90)

    img1 = cv2.imread("top.png")
    img2 = cv2.imread("display.png")
    img3 = cv2.imread("bottom.png")

    list_of_images = [img1, img2, img3]
    interpolation = cv2.INTER_CUBIC

    w_min = min(im.shape[1] for im in list_of_images)
    im_resize_image = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                       for im in list_of_images]
    concate = cv2.vconcat(im_resize_image)

    save_file = cv2.imwrite('qrcode.png', concate)
    time.sleep(3)

    generated_qrcode = send_file('qrcode.png', as_attachment=True)
    return generated_qrcode


if __name__ == "__main__":
    app.run(debug=True)
