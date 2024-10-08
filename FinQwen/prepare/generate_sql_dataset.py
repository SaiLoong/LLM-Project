# -*- coding: utf-8 -*-
# @file generate_sql_dataset.py
# @author zhangshilong
# @date 2024/7/19

from ..tools.config import Config
from ..tools.sql_generator import Manager
from ..tools.utils import File

# 先人工为57个聚类的问题编写对应的Generator放到tools.sql_generator.py, 并利用export方法校验正确性


# =====================================================================================================
# 输出整体校验结果
Manager.analysis()
"""
data_query预计得分: 97.24

丢分超过0.1的Generator:
[4] 4.38/4.5
[11] 1.55/1.67
[12] 3.21/3.33
[17] 3.16/3.33
[21] 1.21/1.67
[28a] 1.56/1.67
[28b] 0.06/0.17
[35b] 0.06/0.17
[40] 1.49/1.67
"""
# 实测97.22


# =====================================================================================================
# 生成600条SQL问题的submit_result.jsonl，耗时10:20
Manager.export_submit_result()

# =====================================================================================================
# 生成nl2sql数据集
train_df = Manager.generate_nl2sql_dataset(Config.NL2SQL_TRAIN_DATASET_NUM)
File.dataframe_to_csv(train_df, Config.NL2SQL_TRAIN_DATASET_PATH)

validation_df = Manager.generate_nl2sql_dataset(Config.NL2SQL_VALIDATION_DATASET_NUM)
File.dataframe_to_csv(validation_df, Config.NL2SQL_VALIDATION_DATASET_PATH)

test_df = Manager.generate_nl2sql_dataset(Config.NL2SQL_TEST_DATASET_NUM)
File.dataframe_to_csv(test_df, Config.NL2SQL_TEST_DATASET_PATH)

# =====================================================================================================
# 生成sql_answer的prompt example
example_df = Manager.generate_sql_prompt_example(Config.SQL_PROMPT_EXAMPLE_NUM)
File.dataframe_to_csv(example_df, Config.SQL_PROMPT_EXAMPLE_PATH)
