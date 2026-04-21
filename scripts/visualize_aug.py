import cv2
import os
import random

IMG_DIR = r"D:\Projects\dl-2026-04\data\processed\images\train"
LBL_DIR = r"D:\Projects\dl-2026-04\data\processed\labels\train"
SAVE_DIR = r"D:\Projects\dl-2026-04\figures\augmentation_examples"

os.makedirs(SAVE_DIR, exist_ok=True)


def draw_boxes(img, labels):
    h, w = img.shape[:2]
    for cls, x, y, bw, bh in labels:
        x1 = int((x - bw / 2) * w)
        y1 = int((y - bh / 2) * h)
        x2 = int((x + bw / 2) * w)
        y2 = int((y + bh / 2) * h)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img


def load_labels(path):
    labels = []
    with open(path, "r") as f:
        for line in f:
            cls, x, y, w, h = map(float, line.strip().split())
            labels.append([cls, x, y, w, h])
    return labels


# 简单增强（翻转）
def horizontal_flip(img, labels):
    img = cv2.flip(img, 1)
    for l in labels:
        l[1] = 1 - l[1]  # x变换
    return img, labels


# 亮度增强
def brightness(img):
    factor = random.uniform(0.5, 1.5)
    img = cv2.convertScaleAbs(img, alpha=factor, beta=0)
    return img


images = os.listdir(IMG_DIR)

for i in range(10):  # 生成10张就够交作业
    name = random.choice(images)

    img_path = os.path.join(IMG_DIR, name)
    lbl_path = os.path.join(LBL_DIR, name.replace(".jpg", ".txt"))

    if not os.path.exists(lbl_path):
        continue

    img = cv2.imread(img_path)
    labels = load_labels(lbl_path)

    # 原图
    img_raw = draw_boxes(img.copy(), labels.copy())

    # 增强
    img_aug, labels_aug = horizontal_flip(img.copy(), [l.copy() for l in labels])
    img_aug = brightness(img_aug)
    img_aug = draw_boxes(img_aug, labels_aug)

    # 拼接
    combined = cv2.hconcat([img_raw, img_aug])

    save_path = os.path.join(SAVE_DIR, f"aug_{i}.jpg")
    cv2.imwrite(save_path, combined)

print("Done!")