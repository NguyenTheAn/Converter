import os
import json
import glob
import pycocotools.coco as coco
from tqdm import tqdm
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', type=str)
parser.add_argument('--annotations_file', type=str)
parser.add_argument('--output_folder', type=str)
parser.add_argument('--output_h', type=int)
parser.add_argument('--output_w', type=int)
parser.add_argument('--keep_size', action="store_true")

args = parser.parse_args()


def load_annotations(img_id):
    ann_ids = coco.getAnnIds(imgIds=[img_id])
    anns = coco.loadAnns(ids=ann_ids) # list type
    return anns

os.makedirs(f"{args.output_folder}/labels", exist_ok=True)

coco = coco.COCO(args.annotations_file)
images = coco.getImgIds()
img_dir = args.image_folder

for image_id in tqdm(images):
    image_info = coco.loadImgs(ids=[image_id])[0]
    file_name = image_info['file_name']
    height, width = image_info['height'], image_info['width']
    args.output_w = width
    args.output_h = height
    img_path = os.path.join(img_dir, file_name)
    anns = load_annotations(image_id)

    x_ratio = 1.0
    y_ratio = 1.0

    if not args.keep_size:
        image = cv2.imread(img_path)
        image = cv2.resize(image, dsize = (args.output_w, args.output_h))
        x_ratio = args.output_w/width
        y_ratio = args.output_h/height
        os.makedirs(f"{args.output_folder}/images", exist_ok=True)
        cv2.imwrite(f"{args.output_folder}/images/{file_name}", image)

    if len(anns) == 0:
        continue
    name = file_name.split(".")[0]
    with open(f"{args.output_folder}/labels/" + name + ".txt", 'w') as file:
        for anno in anns:
            category_id = anno['category_id']
            x, y, w, h = anno['bbox']
            x, y, w, h = round(x*x_ratio), round(y*y_ratio), round(w*x_ratio), round(h*y_ratio)

            xc, yc = x + w//2, y+h//2
            xc, yc, w, h = xc/args.output_w, yc/args.output_h, w/args.output_w, h/args.output_h
            file.write(f"{str(category_id)} {xc} {yc} {w} {h}\n")
