import sys
import cv2
import numpy as np
import os

def process_image(image_path):

    full_path = os.path.join(r"C:\Users\senaa\Downloads\krs-backend-Abdullah", image_path)
    if not os.path.exists(full_path):
        print(f"Dosya bulunamadı: {full_path}")
        return
    
    image = cv2.imread(full_path)
    if image is None:
        print(f"Görüntü yüklenemedi: {full_path}")
        sys.exit(1)

    # Gri tonlamalı formata dönüştür
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gürültüyü azaltmak için bulanıklaştır
    gray = cv2.medianBlur(gray, 5)

    # Hough Daire Dönüşümü ile daireleri tespit et
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=3,
        maxRadius=30
    )

    # Dairelerin koordinatlarını ve yarıçaplarını saklamak için liste oluştur
    circle_coords = []

    # Daireler tespit edildiyse
    if circles is not None:
        # Daire parametrelerini tamsayıya yuvarla
        circles = np.round(circles[0, :]).astype("int")
        # Her bir daire için
        for (x, y, r) in circles:
            circle_coords.append({"x": int(x), "y": int(y), "r": int(r)})

    # JSON formatında çıktı ver
    print({"circles": circle_coords})

    return {"circles": circle_coords}
