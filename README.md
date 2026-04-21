# DL-2026-04 数据集处理与增强作业

## 📌 项目简介
本项目基于 GC10-DET 钢材表面缺陷检测数据集，完成了数据解析、清洗、格式转换、数据增强与可视化，并基于 YOLOv8 进行目标检测训练与结果分析。

---

## 📂 项目结构


dl-2026-04-homework/
├── scripts/              # 数据处理与可视化脚本
├── figures/              # 可视化结果（增强/清洗对比等）
├── runs/                 # YOLO训练结果
├── dataset_report.md     # 数据集处理报告
├── audit_report.md       # 数据审计报告
├── dataset.yaml          # 数据配置文件
└── README.md             # 项目说明


---

## ⚙️ 主要工作内容

### 1. 数据解析
- 将 Pascal VOC（XML）标注解析为 CSV 格式  
- 提取目标框信息（filename, class, xmin, ymin, xmax, ymax）  
- 汇总生成 `raw_annotation_summary.csv`  

---

### 2. 数据清洗
- 删除无法读取的图片（cv2.imread失败）  
- 删除无标注图片  
- 删除异常标注：
  - bbox 宽或高 < 5 像素  
  - bbox 越界  
  - bbox 面积为 0  
- 删除类别异常数据  
- 保证数据规范性与一致性  

---

### 3. 数据转换
- 将标注转换为 YOLO 格式（txt）  
- 对图像进行 padding，使其变为正方形输入  
- 同步更新 bounding box 坐标  

---

### 4. 数据增强
采用多种增强方法提升模型泛化能力：

- 水平翻转（Flip）  
- 亮度/对比度调整  
- 随机缩放（Scale）  
- 随机裁剪（Crop）  
- 轻微旋转（Rotate）  

---

### 5. 可视化分析
生成以下可视化结果：

- 清洗前 vs 清洗后（`figures/cleaning_compare/`）  
- 增强前 vs 增强后（`figures/augmentation_examples/`）  
- 各类别样本展示  

---

### 6. 模型训练
- 使用 YOLOv8 进行目标检测训练  
- 输出训练过程与评估结果：

主要文件：
- `runs/detect/train-3/results.png`  
- `runs/detect/train-3/confusion_matrix.png`  
- `runs/detect/train-3/PR_curve.png`  

---

## 📊 实验结果说明

- 模型已成功收敛  
- 各类别检测效果稳定  
- 无明显异常类别偏差  

---

## 📎 提交说明

- 本项目**不包含原始数据集**（体积较大）  
- 仅提交：
  - 数据处理流程  
  - 可视化结果  
  - 模型训练结果  
- 所有流程均可复现  

---

## 👤 作者：黄彦泽
DL-2026 课程作业
