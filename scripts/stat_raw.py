import pandas as pd

csv_path = r"D:\Projects\dl-2026-04\data\raw_annotation_summary.csv"

df = pd.read_csv(csv_path)

# ===== 总标注数 =====
total_annotations = len(df)

# ===== 有标注图像数 =====
images_with_labels = df["filename"].nunique()

# ===== 原始图像总数 =====
# 👉 直接统计 raw 文件夹
import os
raw_img_dir = r"D:\Projects\dl-2026-04\data\raw\JPEGImages"
total_images = len(os.listdir(raw_img_dir))

# ===== 无标注图像数 =====
images_without_labels = total_images - images_with_labels

print("原始图像总数:", total_images)
print("有标注图像数:", images_with_labels)
print("无标注图像数:", images_without_labels)
print("总标注数量:", total_annotations)