import os
import json
import glob
import cv2
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', type=str)
parser.add_argument('--label_folder', type=str)
parser.add_argument('--show_image', action="store_true")
parser.add_argument('--save_image', action="store_true")
args = parser.parse_args()

bdi_images = glob.glob(args.image_folder + "/*")
label_path = args.label_folder

for i, image_path in tqdm(enumerate(bdi_images)):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    name = os.path.basename(image_path).split(".")[0]
    with open(label_path + name + ".txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split(" ")
            category_id = int(line[0])
            cx, cy, w, h = line[1:]
            cx = round(float(cx) * width)
            cy = round(float(cy) * height)
            w = round(float(w) * width)
            h = round(float(h) * height)
            image = cv2.rectangle(image, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), (0, 255, 0), 1)
            # print(f"{cx} {cy} {h} {w}")
        if args.show_image:
            cv2.imshow("image", image)
            k = cv2.waitKey(0)
            if k == ord("q"):
                cv2.destroyAllWindows()
                break
    if args.save_image:
        os.makedirs("test", exist_ok = True)
        cv2.imwrite("test/" + os.path.basename(image_path), image)
