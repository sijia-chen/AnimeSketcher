import cv2, os
import numpy as np

def invertColor(img):
    return 255 - img

def colorDodge(base, mix):
    base_i32 = base.astype(np.int32)
    mix_i32 = mix.astype(np.int32)
    divisor = 255 - mix
    posto255 = divisor == 0
    divisor[posto255] = 1
    ret = base_i32 + (base_i32 * mix_i32) / divisor
    ret[posto255] = 255
    ret[ret > 255] = 255
    return ret.astype(np.uint8)

def sobel(img):

    img_x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize=1, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    img_y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize=1, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)

    abs_img_x = cv2.convertScaleAbs(img_x)
    abs_img_y = cv2.convertScaleAbs(img_y)

    res = cv2.addWeighted(abs_img_x, 0.5, abs_img_y, 0.5, 0)
    return invertColor(res)

def threshold(img, threshold = 240):
    img[img>threshold] = 255

def enhance(img, threshold = 240, alpha = 0.8):
    pos = img <= threshold
    img = img.astype(np.float32)
    img[pos] *= alpha
    return img.astype(np.uint8)

def sketch(img, mode = 'sobel'):
    if mode == 'sobel':
        s = sobel(img)
        threshold(s)
        return s
    elif mode == 'erode':
        ivt = invertColor(img)
        mix = cv2.erode(ivt, (3,3), iterations=2)
        # mix = cv2.GaussianBlur(ivt, (3, 3), 2, 2)
        cd = colorDodge(img, mix)
        threshold(cd)
        return enhance(cd)

if __name__ == '__main__':
    gray = cv2.imread('a.jpg', 0)
    skt = sketch(gray, 'sobel')
