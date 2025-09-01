#!/bin/bash
# 定义Hive数据库名称
HIVE_DB="city_db"
# 统计结果HDFS路径
HDFS_RESULT_PATH="/data/city_stat_result"
# 本地临时文件路径
LOCAL_TMP_FILE="/tmp/city_stat.csv"

# MySQL连接配置
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASS="123456"
MYSQL_DB="city_stats"
MYSQL_TABLE="city_statistics"

# Step 1: 在Hive中执行统计查询
echo "正在执行Hive统计查询..."
hive -e "
USE ${HIVE_DB};

INSERT OVERWRITE DIRECTORY '${HDFS_RESULT_PATH}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT 
    adcode,
    SUM(CASE WHEN gender = 0 THEN 1 ELSE 0 END) AS male_count,   -- 0代表男性
    SUM(CASE WHEN gender = 1 THEN 1 ELSE 0 END) AS female_count, -- 1代表女性
    SUM(CASE WHEN age BETWEEN 0 AND 18 THEN 1 ELSE 0 END) AS age_0_18,
    SUM(CASE WHEN age BETWEEN 19 AND 45 THEN 1 ELSE 0 END) AS age_19_45,
    SUM(CASE WHEN age BETWEEN 46 AND 60 THEN 1 ELSE 0 END) AS age_46_60,
    SUM(CASE WHEN age > 60 THEN 1 ELSE 0 END) AS age_60_plus
FROM city_textfile
GROUP BY adcode;
"

# Step 2: 将HDFS结果拉到本地
echo "导出HDFS统计结果到本地..."
hdfs dfs -getmerge ${HDFS_RESULT_PATH}/* ${LOCAL_TMP_FILE}

# Step 3: 创建MySQL数据库和表
echo "创建MySQL数据库和表..."
mysql -h ${MYSQL_HOST} -P ${MYSQL_PORT} -u ${MYSQL_USER} -p${MYSQL_PASS} <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DB};
USE ${MYSQL_DB};

CREATE TABLE IF NOT EXISTS ${MYSQL_TABLE} (
    adcode VARCHAR(20) PRIMARY KEY COMMENT '行政区划代码',
    male_count INT COMMENT '男性数量',
    female_count INT COMMENT '女性数量',
    age_0_18 INT COMMENT '0-18岁数量',
    age_19_45 INT COMMENT '19-45岁数量',
    age_46_60 INT COMMENT '46-60岁数量',
    age_60_plus INT COMMENT '60岁以上数量',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
EOF

# Step 4: 导入数据到MySQL
echo "导入数据到MySQL..."
mysql -h ${MYSQL_HOST} -P ${MYSQL_PORT} -u ${MYSQL_USER} -p${MYSQL_PASS} ${MYSQL_DB} <<EOF
LOAD DATA LOCAL INFILE '${LOCAL_TMP_FILE}'
INTO TABLE ${MYSQL_TABLE}
FIELDS TERMINATED BY ','
(adcode, male_count, female_count, age_0_18, age_19_45, age_46_60, age_60_plus)
SET update_time = CURRENT_TIMESTAMP;
EOF

# Step 5: 清理临时文件
echo "清理临时文件..."
rm -f ${LOCAL_TMP_FILE}
hdfs dfs -rm -r ${HDFS_RESULT_PATH}

echo "数据统计并同步到MySQL完成！"
