import cv2
import numpy as np

n = 1  # 采样数

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# flag = cap.isOpened()
bri = np.zeros(n, np.int_)

for i in range(n):
    success, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    H, S, V = cv2.split(hsv)
    v = V.ravel()[np.flatnonzero(V)]  # 亮度非零的值
    bri[i] = sum(v) / len(v)
print(sum(bri) / len(bri))

# 关闭摄像头
cap.release()
