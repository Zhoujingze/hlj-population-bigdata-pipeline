#!/bin/bash
# 定义Hive数据库名称
DB_NAME="city_db"
# 原始数据路径
HDFS_DATA_PATH="/data/cityFile/city.txt"

# 创建Hive数据库（如果不存在）
hive -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Step 1: 创建Hive表（TextFile、RCFile、ORC格式）
hive -e "
-- 创建TextFile格式表
CREATE TABLE IF NOT EXISTS ${DB_NAME}.city_textfile (
    phone STRING,
    age INT,
    gender INT,
    adcode STRING,
    dummy INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/city_textfile';

-- 创建RCFile格式表
CREATE TABLE IF NOT EXISTS ${DB_NAME}.city_rcfile (
    phone STRING,
    age INT,
    gender INT,
    adcode STRING,
    dummy INT
)
STORED AS RCFILE
LOCATION '/user/hive/warehouse/city_rcfile';

-- 创建ORC格式表
CREATE TABLE IF NOT EXISTS ${DB_NAME}.city_orc (
    phone STRING,
    age INT,
    gender INT,
    adcode STRING,
    dummy INT
)
STORED AS ORC
LOCATION '/user/hive/warehouse/city_orc';
"

# Step 2: 加载数据到TextFile表
hive -e "
LOAD DATA INPATH '${HDFS_DATA_PATH}' OVERWRITE INTO TABLE ${DB_NAME}.city_textfile;
"

# Step 3: 转换数据到RCFile和ORC表
hive -e "
-- 插入数据到RCFile表
INSERT OVERWRITE TABLE ${DB_NAME}.city_rcfile
SELECT * FROM ${DB_NAME}.city_textfile;

-- 插入数据到ORC表
INSERT OVERWRITE TABLE ${DB_NAME}.city_orc
SELECT * FROM ${DB_NAME}.city_textfile;
"

# Step 4: 查看表占用空间大小
echo -e "\n===== 表存储空间大小 =====\n"

# 获取表路径并计算大小
for table in city_textfile city_rcfile city_orc; do
    TABLE_PATH="/user/hive/warehouse/${table}"
    echo "表名: ${table}"
    hdfs dfs -du -h ${TABLE_PATH}
    echo "------------------------"
done
