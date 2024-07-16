# -*- coding: utf-8 -*-
# @file generate_sql_test_question.py
# @author zhangshilong
# @date 2024/7/12

from ..tools.config import Config

db = Config.get_database()

# =====================================================================================================
# 统一规范：
# 1. 为了防止有冗余数据（同时也不想逐条检查），所有COUNT都加上DISTINCT
# 2. 所有sql均以'LIMIT XX;'结尾，哪怕只有一条数据也要加
# 3. 子查询根据需求使用LIMIT, 如果是单条, WHERE用=而不是IN
# 4. 只有 基金基本信息 确认不存在数据重复，其它表的查询结果难以保证（虽然暂时未发现），因此计算COUNT时尽量加上DISTINCT

"""
基金基本信息：
    主键：基金代码、基金全称、基金简称（三个都行）
    管理费率、托管费率：取值形如 '1.2%', 经测试可以直接比较（如 管理费率 < '0.8%' ）
    

基金股票持仓明细：
    主键：基金代码 + 持仓日期 + 报告类型 + 第N大重仓股
            934514组唯一，10629组重复（股票代码以及相关数据不同），题目貌似暂时未遇到，忽略不考虑
        基金代码 + 持仓日期 + 报告类型 + 股票代码
            949869组唯一，397组重复，忽略不考虑
    股票代码：既可能在 A股票日行情表、也可能在 港股票日行情表 上！
    持仓日期：将初步分析，部分 报告类型 = '季报'、'年报(含半年报)' 的基金虽然可能有不在季末的报告，但季末一定有报告。因此取条件时直接以季末为准


基金债券持仓明细：
    主键：基金代码 + 持仓日期 + 报告类型 + 第N大重仓股
        基金代码 + 持仓日期 + 报告类型 + 债券名称

 
基金可转债持仓明细：
    主键：基金代码 + 持仓日期 + 报告类型 + 第N大重仓股
        基金代码 + 持仓日期 + 报告类型 + 对应股票代码
            有74665组唯一，751+8+8组重复，忽略不考虑
    对应股票代码：只有A股，没有港股
    持仓日期：将初步分析，部分 报告类型 = '季报' 的基金虽然可能有不在季末的报告，但季末一定有报告。因此取条件时直接以季末为准


基金日行情表：
    主键：基金代码 + 交易日期


A股票日行情表：
    主键：股票代码 + 交易日
    股票代码：与 港股票日行情表 的 股票代码 没有重叠    
    
    
港股票日行情表：
    主键：股票代码 + 交易日
        只有'13 HK', '1997 HK', '20 HK', '382 HK', '816 HK'这五只股票的数据重复，忽略不考虑
    股票代码：与 A股票日行情表 的 股票代码 没有重叠


A股公司行业划分表：
    主键：股票代码 + 交易日期 + 行业划分标准
    股票代码：只有A股，没有港股
    行业划分标准=中信/申万行业分类 下，有部分一级行业名称（例如 汽车 计算机）会重叠


基金规模变动表：
    主键：基金代码 + 截止日期
    截止日期：月日的组合只有4种可能（季末），连同年一共只有12种取值


基金份额持有人结构：
    主键：基金代码 + 截止日期 、 基金代码 + 定期报告所属年度 + 报告类型（两组都行）
    个人/机构投资者持有的基金份额占总份额比例：是[0, 100]的数字
    报告类型='年度报告'的截止日期一定是12-31，报告类型='中期报告'的截止日期一定是06-30
"""

# =====================================================================================================
# 多进程要求很多：
#   1. sqlite3.Connection不能pickle，因此必须每个进程重新连接
#   2. 加了@cache的实例不能pickle
#   3. 其实前两个还好，主要是notebook跑多进程好像有问题，同样的代码每跑10次有1-2次会卡住，而且还是一开始就卡住


# TODO 可能有的问题：
#  聚类13没有明确是A股还是港股（但感觉是A股）
#  所有用到 基金股票持仓明细、基金可转债持仓明细 报告日期的sql，日期不对（但应该不可能）
