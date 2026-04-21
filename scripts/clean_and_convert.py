import os
import cv2
import pandas as pd
from tqdm import tqdm

# 路径
csv_path = r"D:\Projects\dl-2026-04\data\raw_annotation_summary.csv"
img_dir = r"D:\Projects\dl-2026-04\data\raw\JPEGImages"
save_img_dir = r"D:\Projects\dl-2026-04\data\processed\images\train"
save_label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\train"

os.makedirs(save_img_dir, exist_ok=True)
os.makedirs(save_label_dir, exist_ok=True)

# 读取CSV
df = pd.read_csv(csv_path)

# 类别映射
classes = sorted(df["class"].unique())
class_map = {c: i for i, c in enumerate(classes)}

print("类别映射：", class_map)

# 分组
grouped = df.groupby("filename")

# 主循环（⚠️ 只有这一层！）
for img_name, group in tqdm(grouped):

    # 修复文件名
    img_name = img_name.replace(".jpg.jpg", ".jpg").strip()

    if not img_name.endswith(".jpg"):
        continue

    img_path = os.path.join(img_dir, img_name)

    if not os.path.exists(img_path):
        print("文件不存在:", img_path)
        continue

    img = cv2.imread(img_path)

    if img is None:
        print("坏图:", img_path)
        continue

    h, w = img.shape[:2]

    yolo_labels = []

    # 遍历当前图片的标注
    for _, row in group.iterrows():

        xmin, ymin, xmax, ymax = row[["xmin", "ymin", "xmax", "ymax"]]

        bw = xmax - xmin
        bh = ymax - ymin

        if bw <= 5 or bh <= 5:
            continue

        if xmin < 0 or ymin < 0 or xmax > w or ymax > h:
            continue

        x_center = (xmin + xmax) / 2 / w
        y_center = (ymin + ymax) / 2 / h
        bw /= w
        bh /= h

        cls_id = class_map[row["class"]]

        yolo_labels.append(f"{cls_id} {x_center} {y_center} {bw} {bh}")

    if len(yolo_labels) == 0:
        continue

    # 保存图片
    save_img_path = os.path.join(save_img_dir, img_name)
    cv2.imwrite(save_img_path, img)

    # 保存标签
    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(save_label_dir, label_name)

    with open(label_path, "w") as f:
        f.write("\n".join(yolo_labels))

print("✅ 清洗+转换完成")