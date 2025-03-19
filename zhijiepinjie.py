# 在一个新的.py文件中，比如match_images.py

import cv2
import numpy as np
import sys

def match_images(image_path_A, image_path_B):
    # 导入图像
    ima = cv2.imread(image_path_A)
    imb = cv2.imread(image_path_B)
    A = ima.copy()
    B = imb.copy()
    imageA = cv2.resize(A, (0, 0), fx=0.2, fy=0.2)
    imageB = cv2.resize(B, (0, 0), fx=0.2, fy=0.2)

    # 检测A、B图片的SIFT关键特征点，并计算特征描述子
    def detectAndDescribe(image):
        sift = cv2.SIFT_create()
        (kps, features) = sift.detectAndCompute(image, None)
        kps = np.float32([kp.pt for kp in kps])
        return (kps, features)

    kpsA, featuresA = detectAndDescribe(imageA)
    kpsB, featuresB = detectAndDescribe(imageB)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(featuresA, featuresB, 2)
    good = []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * 0.75:
            good.append((m[0].trainIdx, m[0].queryIdx))

    if len(good) > 4:
        ptsA = np.float32([kpsA[i] for (_, i) in good])
        ptsB = np.float32([kpsB[i] for (i, _) in good])
        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)

    M = (matches, H, status)
    if M is None:
        print("无匹配结果")
        sys.exit()

    (matches, H, status) = M
    result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
    result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

    return result

# 调用示例
# if __name__ == "__main__":
#     result_image = match_images("C:\\Users\\86155\\Desktop\\you.jpg", "C:\\Users\\86155\\Desktop\\zuo.jpg")
#     cv2.imshow('Result', result_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
