import cv2
import numpy as np


def dodgeV2(image, mask):
    return cv2.divide(image, 255 - mask, scale=256)


def rgb_to_sketch(src_image_name, dst_image_name):
    img_rgb = cv2.imread(src_image_name)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21),
                                sigmaX=0, sigmaY=0)
    img_blend = dodgeV2(img_gray, img_blur)

    cv2.imshow("pencil sketch", img_blend)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(dst_image_name, img_blend)


# if __name__ == '__main__':
#     src_image_name = "C:\\Users\\86155\\Desktop\\image2.png"
#     dst_image_name = 'sketch_example.jpg'
#     rgb_to_sketch(src_image_name, dst_image_name)
