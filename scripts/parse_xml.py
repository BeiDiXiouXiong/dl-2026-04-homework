import os
import xml.etree.ElementTree as ET
import pandas as pd

xml_dir = "data/raw/Annotations"
records = []

for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(xml_dir, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    filename = root.find("filename").text

    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    for obj in root.findall("object"):
        cls = obj.find("name").text

        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        records.append([
            filename, width, height,
            cls, xmin, ymin, xmax, ymax
        ])

df = pd.DataFrame(records, columns=[
    "filename", "width", "height",
    "class", "xmin", "ymin", "xmax", "ymax"
])

os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_annotation_summary.csv", index=False)

output_path = r"D:\Projects\dl-2026-04\data\raw_annotation_summary.csv"
df.to_csv(output_path, index=False)

print("✅ 解析完成！")
print("📂 保存路径：", output_path)
print("📊 标注数量：", len(df))