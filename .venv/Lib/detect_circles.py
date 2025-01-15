import sys
import cv2
import numpy as np
import os
import requests

def process_image(image_url):

    response = requests.get(image_url)
    
    if response.status_code != 200:
        print(f"Image didn't download: {image_url}")
        sys.exit(1)
    
    image_array = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        print("Image didn't upload.")
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
