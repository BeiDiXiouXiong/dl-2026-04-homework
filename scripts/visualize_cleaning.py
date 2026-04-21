import os
import cv2
import random
import pandas as pd

# ===== 路径 =====
raw_img_dir = r"D:\Projects\dl-2026-04\data\raw\JPEGImages"
raw_csv = r"D:\Projects\dl-2026-04\data\raw_annotation_summary.csv"

processed_img_dir = r"D:\Projects\dl-2026-04\data\processed\images\train"
processed_label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\train"

save_dir = r"D:\Projects\dl-2026-04\figures\cleaning_compare"
os.makedirs(save_dir, exist_ok=True)

# ===== 读取原始标注 =====
df = pd.read_csv(raw_csv)

# ===== ⭐关键：从 processed 里选，保证一定存在 =====
all_images = os.listdir(processed_img_dir)
sample_images = random.sample(all_images, min(10, len(all_images)))

def draw_raw_boxes(img, group):
    for _, row in group.iterrows():
        xmin, ymin, xmax, ymax = map(int, row[["xmin", "ymin", "xmax", "ymax"]])
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
    return img

def draw_yolo_boxes(img, label_path):
    if not os.path.exists(label_path):
        return img

    h, w = img.shape[:2]

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        cls, x, y, bw, bh = map(float, line.strip().split())

        xmin = int((x - bw/2) * w)
        ymin = int((y - bh/2) * h)
        xmax = int((x + bw/2) * w)
        ymax = int((y + bh/2) * h)

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    return img

for img_name in sample_images:

    name = os.path.splitext(img_name)[0]

    # ===== 原始 =====
    raw_path = os.path.join(raw_img_dir, name + ".jpg")
    if not os.path.exists(raw_path):
        raw_path = os.path.join(raw_img_dir, name + ".png")

    if not os.path.exists(raw_path):
        print(f"❌ raw缺失: {img_name}")
        continue

    raw_img = cv2.imread(raw_path)
    group = df[df["filename"].str.contains(name)]

    raw_img = draw_raw_boxes(raw_img.copy(), group)

    # ===== 清洗后 =====
    proc_path = os.path.join(processed_img_dir, img_name)
    label_path = os.path.join(processed_label_dir, name + ".txt")

    if not os.path.exists(proc_path):
        print(f"❌ processed缺失: {img_name}")
        continue

    proc_img = cv2.imread(proc_path)
    proc_img = draw_yolo_boxes(proc_img.copy(), label_path)

    # ===== 拼接 =====
    raw_img = cv2.resize(raw_img, (512, 512))
    proc_img = cv2.resize(proc_img, (512, 512))

    compare = cv2.hconcat([raw_img, proc_img])

    # ===== 保存 =====
    cv2.imwrite(os.path.join(save_dir, f"{name}_before.jpg"), raw_img)
    cv2.imwrite(os.path.join(save_dir, f"{name}_after.jpg"), proc_img)
    cv2.imwrite(os.path.join(save_dir, f"{name}_compare.jpg"), compare)

    print(f"✅ 已生成: {name}")

print("🎉 清洗前 vs 清洗后 对比图已生成")