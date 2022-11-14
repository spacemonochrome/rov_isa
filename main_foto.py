import cv2
import numpy as np
import detector_code

prev_frame_time = 0
new_frame_time = 0

roi = cv2.imread("u.png")
color_g = np.array([20,30,30]), np.array([85,255,255])
resim_yukseklik, resim_genislik, _ = roi.shape
roi = detector_code.kamera_islem(roi)

roi = detector_code.kamera_xy_cizgi( roi)
fps, prev_frame_time, new_frame_time = detector_code.fps_func(prev_frame_time,new_frame_time)

cv2.putText(roi, fps + " FPS", (15,15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 1, cv2.LINE_AA)

cv2.imshow('tespit',roi)
cv2.imwrite('cikti.png',roi)
cv2.waitKey()
     
    
    