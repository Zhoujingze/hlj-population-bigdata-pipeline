import os


def merge_files(input_dir, output_file):
    """
    合并指定目录下的所有.txt文件到一个输出文件中。

    :param input_dir: 包含.txt文件的目录
    :param output_file: 合并后的输出文件路径
    """
    # 确保输入目录存在
    if not os.path.exists(input_dir):
        print(f"错误：目录 {input_dir} 不存在！")
        return

    # 获取目录下所有.txt文件
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    if not txt_files:
        print(f"警告：目录 {input_dir} 中没有找到任何.txt文件！")
        return

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for txt_file in txt_files:
            file_path = os.path.join(input_dir, txt_file)
            # 打开每个.txt文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content + '\n')  # 写入内容并添加换行符

    print(f"所有文件已合并到 {output_file}")


def count_lines(file_path):
    """
    统计文件中的总行数。

    :param file_path: 文件路径
    :return: 文件中的总行数
    """
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在！")
        return 0

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return len(lines)


def main():
    # 配置参数
    input_dir = r"E:\PythonProject\课程设计\code\data"  # 输入目录
    output_file = r"E:\PythonProject\课程设计\code\data\黑龙江省.txt"  # 输出文件

    # 调用合并函数
    merge_files(input_dir, output_file)

    # 统计合并后的文件中的总条数
    total_lines = count_lines(output_file)
    print(f"合并后的文件 {output_file} 中的总条数为：{total_lines}")


if __name__ == "__main__":
    main()