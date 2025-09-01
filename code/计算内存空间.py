import os

# 定义存放文件的文件夹路径
data_folder = r"城市人口数据采集系统以黑龙江省为例\code\data"

# 检查文件夹是否存在
if not os.path.exists(data_folder):
    print(f"文件夹 '{data_folder}' 不存在，请确保文件夹路径正确且文件已生成。")
else:
    # 遍历文件夹中的所有文件
    for filename in os.listdir(data_folder):
        # 构造完整的文件路径
        file_path = os.path.join(data_folder, filename)

        # 确保是文件
        if os.path.isfile(file_path):
            # 获取文件大小（字节）
            file_size_bytes = os.path.getsize(file_path)
            # 转换为MB
            file_size_mb = file_size_bytes / (1024 * 1024)

            # 打印文件名和大小
            print(f"文件：{filename}，大小：{file_size_bytes} 字节 ({file_size_mb:.2f} MB)")