import os
import pandas as pd
import numpy as np
from collections import defaultdict

# 配置参数
DATA_DIR = "data"
EXCEL_PATH = "城市人口数据采集系统以黑龙江省为例\data\黑龙江.xlsx"  # 使用相对路径
CITY_INFO = [
    {'城市': '哈尔滨市', '人口数': 10009900, '代码': '2301', '手机号头': '138'},
    {'城市': '绥化市', '人口数': 3756200, '代码': '2312', '手机号头': '130'},
    {'城市': '齐齐哈尔市', '人口数': 4067500, '代码': '2302', '手机号头': '136'},
    {'城市': '大庆市', '人口数': 2781600, '代码': '2306', '手机号头': '150'},
    {'城市': '牡丹江市', '人口数': 2290200, '代码': '2310', '手机号头': '166'},
    {'城市': '佳木斯市', '人口数': 2156500, '代码': '2308', '手机号头': '154'},
    {'城市': '鸡西市', '人口数': 1502100, '代码': '2303', '手机号头': '137'},
    {'城市': '黑河市', '人口数': 1286400, '代码': '2311', '手机号头': '132'},
    {'城市': '双鸭山市', '人口数': 1208800, '代码': '2305', '手机号头': '189'},
    {'城市': '鹤岗市', '人口数': 891300, '代码': '2304', '手机号头': '139'},
    {'城市': '伊春市', '人口数': 878900, '代码': '2307', '手机号头': '151'},
    {'城市': '七台河市', '人口数': 689600, '代码': '2309', '手机号头': '155'},
    {'城市': '大兴安岭地区', '人口数': 331300, '代码': '2327', '手机号头': '131'},
]

def main():
    # 检查Excel文件是否存在
    if not os.path.exists(EXCEL_PATH):
        print(f"错误：文件 {EXCEL_PATH} 不存在！")
        exit()

    # 创建数据目录
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        # 读取Excel文件
        df = pd.read_excel(
            EXCEL_PATH,
            dtype={'行政区划代码': str},
            engine='openpyxl'
        )
    except Exception as e:
        print(f"读取Excel失败: {e}")
        exit()

    # 提取有效区划代码
    valid_codes = [
        (row['行政区划代码'], row['行政区名称'].split(',')[-1])
        for _, row in df.iterrows()
        if len(row['行政区划代码']) == 6
    ]

    # 构建城市代码映射
    city_code_map = defaultdict(list)
    code_to_city = {info['代码']: info['城市'] for info in CITY_INFO}

    for code, _ in valid_codes:
        city_code = code[:4]  # 匹配地级市代码
        if city_code in code_to_city:
            city = code_to_city[city_code]
            city_code_map[city].append(code)
        else:
            print(f"警告：区划代码 {code} 未匹配到城市")

    # 为每个城市生成数据
    for city_info in CITY_INFO:
        city = city_info['城市']
        population = city_info['人口数']
        phone_head = city_info['手机号头']
        codes = city_code_map.get(city, [])

        if not codes:
            print(f"跳过 {city}：无有效区划代码")
            continue

        # 检查手机号容量
        max_phones = 10 ** 8  # 8位后缀
        if population > max_phones:
            print(f"错误：{city} 人口超过手机号容量（{max_phones}）")
            continue

        # 生成唯一手机号后缀
        rng = np.random.default_rng()
        suffixes = rng.choice(max_phones, size=population, replace=False)

        # 生成其他字段
        ages = np.random.randint(16, 100, population)
        genders = np.random.randint(0, 2, population)
        selected_codes = np.random.choice(codes, population)

        # 写入文件
        filename = os.path.join(DATA_DIR, f"{city}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(population):
                phone = f"{phone_head}{suffixes[i]:08d}"
                line = f"{phone}|{ages[i]}|{genders[i]}|{selected_codes[i]}|0\n"
                f.write(line)

        print(f"生成完成：{city} ({population} 条数据)")

if __name__ == "__main__":
    main()