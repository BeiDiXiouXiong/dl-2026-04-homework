import os
import random
import shutil

# 路径
img_dir = r"D:\Projects\dl-2026-04\data\processed\images\train"
label_dir = r"D:\Projects\dl-2026-04\data\processed\labels\train"

base_dir = r"D:\Projects\dl-2026-04\data\processed"

# 目标目录
splits = ["train", "val", "test"]

for split in splits:
    os.makedirs(os.path.join(base_dir, "images", split), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "labels", split), exist_ok=True)

# 获取所有图片
images = [f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".png"))]
print("图片数量：", len(images))

# 固定随机种子（评分点）
random.seed(42)
random.shuffle(images)

# 划分比例（你可以写进报告）
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

n = len(images)
train_end = int(n * train_ratio)
val_end = train_end + int(n * val_ratio)

train_imgs = images[:train_end]
val_imgs = images[train_end:val_end]
test_imgs = images[val_end:]

def move_files(img_list, split):
    for img in img_list:
        label = img.replace(".jpg", ".txt")

        shutil.move(
            os.path.join(img_dir, img),
            os.path.join(base_dir, "images", split, img)
        )

        shutil.move(
            os.path.join(label_dir, label),
            os.path.join(base_dir, "labels", split, label)
        )

# 执行移动
move_files(train_imgs, "train")
move_files(val_imgs, "val")
move_files(test_imgs, "test")

print("✅ 数据划分完成")
print(f"train: {len(train_imgs)}")
print(f"val: {len(val_imgs)}")
print(f"test: {len(test_imgs)}")