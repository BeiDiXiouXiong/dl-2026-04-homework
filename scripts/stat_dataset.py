import os
import pandas as pd
from collections import Counter

# ===== 路径 =====
train_label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\train"
val_label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\val"
test_label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\test"

# ===== 统计函数 =====
def analyze_split(label_dir):
    total_images = 0
    total_boxes = 0
    per_image_boxes = []
    class_counter = Counter()

    for file in os.listdir(label_dir):
        if not file.endswith(".txt"):
            continue

        total_images += 1

        with open(os.path.join(label_dir, file)) as f:
            lines = f.readlines()

        total_boxes += len(lines)
        per_image_boxes.append(len(lines))

        for line in lines:
            cls = int(line.split()[0])
            class_counter[cls] += 1

    avg_boxes = total_boxes / total_images if total_images > 0 else 0

    return {
        "images": total_images,
        "boxes": total_boxes,
        "avg": avg_boxes,
        "per_image": per_image_boxes,
        "class_counter": class_counter
    }

# ===== 统计 =====
train_stats = analyze_split(train_label_dir)
val_stats = analyze_split(val_label_dir)
test_stats = analyze_split(test_label_dir)

print("\n===== 按 split 统计 =====")
for name, stats in zip(["train", "val", "test"], [train_stats, val_stats, test_stats]):
    print(f"{name}: 图像={stats['images']} 标注={stats['boxes']} 平均={stats['avg']:.2f}")

# ===== 类别统计 =====
print("\n===== 类别分布（train）=====")
for cls, cnt in train_stats["class_counter"].items():
    print(f"类 {cls}: {cnt}")

# ===== 缺陷数量分布 =====
def count_distribution(per_image):
    d = {"1":0, "2-3":0, "4+":0}
    for n in per_image:
        if n == 1:
            d["1"] += 1
        elif 2 <= n <= 3:
            d["2-3"] += 1
        else:
            d["4+"] += 1
    return d

print("\n===== 每图缺陷数量 =====")
dist = count_distribution(train_stats["per_image"])
print(dist)

# ===== 尺寸分布（small/medium/large）=====
def size_stats(label_dir):
    small, medium, large = 0, 0, 0

    for file in os.listdir(label_dir):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(label_dir, file)) as f:
            lines = f.readlines()

        for line in lines:
            _, _, _, w, h = map(float, line.split())
            area = w * h

            if area < 0.01:
                small += 1
            elif area < 0.05:
                medium += 1
            else:
                large += 1

    return small, medium, large

s, m, l = size_stats(train_label_dir)

print("\n===== 尺寸分布（train）=====")
print(f"small: {s}, medium: {m}, large: {l}")