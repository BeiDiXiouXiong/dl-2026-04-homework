import os
import cv2
import random
from collections import defaultdict

IMG_DIR = r"D:\Projects\dl-2026-04\data\processed\images\train"
LBL_DIR = r"D:\Projects\dl-2026-04\data\processed\labels\train"
SAVE_DIR = r"D:\Projects\dl-2026-04\figures\visualization"

os.makedirs(SAVE_DIR, exist_ok=True)


def draw_boxes(img, labels):
    h, w = img.shape[:2]
    for cls, x, y, bw, bh in labels:
        x1 = int((x - bw / 2) * w)
        y1 = int((y - bh / 2) * h)
        x2 = int((x + bw / 2) * w)
        y2 = int((y + bh / 2) * h)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, str(int(cls)), (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    return img


def load_labels(path):
    labels = []
    with open(path, "r") as f:
        for line in f:
            cls, x, y, w, h = map(float, line.strip().split())
            labels.append([cls, x, y, w, h])
    return labels


# 收集每个类别的图片
class_images = defaultdict(list)

images = os.listdir(IMG_DIR)

for name in images:
    lbl_path = os.path.join(LBL_DIR, name.replace(".jpg", ".txt"))
    if not os.path.exists(lbl_path):
        continue

    labels = load_labels(lbl_path)
    classes = set(int(l[0]) for l in labels)

    for c in classes:
        class_images[c].append(name)


# 1️⃣ 每类5张
for cls, img_list in class_images.items():
    sampled = random.sample(img_list, min(5, len(img_list)))

    for i, name in enumerate(sampled):
        img_path = os.path.join(IMG_DIR, name)
        lbl_path = os.path.join(LBL_DIR, name.replace(".jpg", ".txt"))

        img = cv2.imread(img_path)
        labels = load_labels(lbl_path)

        img = draw_boxes(img, labels)

        save_path = os.path.join(SAVE_DIR, f"class_{cls}_{i}.jpg")
        cv2.imwrite(save_path, img)


# 2️⃣ 随机样本10张
random_samples = random.sample(images, 10)

for i, name in enumerate(random_samples):
    img_path = os.path.join(IMG_DIR, name)
    lbl_path = os.path.join(LBL_DIR, name.replace(".jpg", ".txt"))

    if not os.path.exists(lbl_path):
        continue

    img = cv2.imread(img_path)
    labels = load_labels(lbl_path)

    img = draw_boxes(img, labels)

    save_path = os.path.join(SAVE_DIR, f"random_{i}.jpg")
    cv2.imwrite(save_path, img)


print("✅ visualization 生成完成！")