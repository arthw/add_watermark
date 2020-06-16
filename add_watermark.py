import cv2
import os,sys, glob
import numpy as np
import random

def add_copy(watermark, image, cx, cy):
    (h, w) = image.shape[:2]
    (wH, wW) = watermark.shape[:2]
    # Creating the image's overlay with the watermark
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[cy:wH + cy, cx:wW + cx] = watermark

    # Applying the overlay
    res = image.copy()
    alpha = random.uniform(0.03, 0.06)
    cv2.addWeighted(overlay, alpha, res, 1.0, 0, res)
    return res

def add_watermark(input, output, watermark):
    image = cv2.imread(input)
    (h, w) = image.shape[:2]
    image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])


    # Reading the watermark

    watermark = cv2.imread(watermark, cv2.IMREAD_UNCHANGED)

    (wH, wW) = watermark.shape[:2]
    wh = int(h/10*random.uniform(0.85, 1))
    ww = int(wW/wH*wh)
    print(wH, wW)
    print(wh, ww)

    watermark = cv2.resize(watermark, (ww, wh))
    (wH, wW) = watermark.shape[:2]

    (B, G, R, A) = cv2.split(watermark)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    watermark = cv2.merge([B, G, R, A])

    cy = int(h*0.01*random.uniform(0.85, 1))
    cx = int(w*0.01*random.uniform(0.85, 1))
    res = add_copy(watermark, image, cx, cy)

    cy = int((h-wH) * 0.98*random.uniform(0.85, 1))
    cx = int((w-wW) * 0.98*random.uniform(0.85, 1))
    res = add_copy(watermark, res, cx, cy)

    cy = int((h) * 0.01*random.uniform(0.85, 1))
    cx = int((w-wW) * 0.98*random.uniform(0.85, 1))
    res = add_copy(watermark, res, cx, cy)

    cy = int((h-wH) * 0.98*random.uniform(0.85, 1))
    cx = int((w) * 0.01*random.uniform(0.85, 1))
    res = add_copy(watermark, res, cx, cy)

    cv2.imwrite(output, res)

def main(input_folder, output_folder, string):
    for input in glob.glob(input_folder+"/*.jpg"):
        _, filename = os.path.split(input)
        print(filename)
        output = os.path.join(output_folder,filename)
        print(output)
    add_watermark(input, output, string)
def help():
    print("Miss parameters: input_folder output_folder watermark.jpg")

if __name__ == "__main__":
    if len(sys.argv)<4:
        help()
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    watermark = sys.argv[3]
    main(input_folder, output_folder, watermark)
