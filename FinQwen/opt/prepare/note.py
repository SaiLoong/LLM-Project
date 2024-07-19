# -*- coding: utf-8 -*-
# @file note.py
# @author zhangshilong
# @date 2024/7/12


# =====================================================================================================
# 统一规范：
# 1. 所有sql均以'LIMIT XX;'结尾，哪怕只有一条数据也要加
# 2. 联合查询如果只是涉及一个连接条件且比较简单，可以用WHERE IN，否则应该用JOIN ON语法

# 刷分经验
# 1. 除非题目明确提到港股，一般不用考虑港股
# 2. 如果题目要求百分数保留两位小数，哪怕答案刚好是2%，也要写成2.00%

1

"""
基金基本信息：
    主键：基金代码、基金全称、基金简称（三个都行）
    管理费率、托管费率：取值形如 '1.2%', 经测试可以直接比较（如 管理费率 < '0.8%' ）
    

基金股票持仓明细：
    主键：基金代码 + 持仓日期 + 报告类型 + 第N大重仓股
            934514组唯一，10629组重复（股票代码以及相关数据不同），题目貌似暂时未遇到，忽略不考虑
            无法确定固定 基金代码 + 持仓日期 + 报告类型 下，第N大重仓股 是否与 市值 的序关系是一致的
        基金代码 + 持仓日期 + 报告类型 + 股票代码
            949869组唯一，397组重复，忽略不考虑
    股票代码：既可能在 A股票日行情表、也可能在 港股票日行情表 上！
    持仓日期：将初步分析，部分 报告类型 = '季报'、'年报(含半年报)' 的基金虽然可能有不在季末的报告，但季末一定有报告。因此取条件时直接以季末为准


基金债券持仓明细：
    主键：基金代码 + 持仓日期 + 报告类型 + 第N大重仓股
        基金代码 + 持仓日期 + 报告类型 + 债券名称
    持仓日期：报告类型 = '年报(含半年报)'的记录大部分在0630、1231，只有小部分不在

 
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
    净赎回 = 报告期期初基金总份额 - 报告期期末基金总份额
        不要用 报告期基金总赎回份额 - 报告期基金总申购份额，这两个值可能都为0.0，不可信
        同理，净申购 = 报告期期末基金总份额 - 报告期期初基金总份额


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


# TODO 如果回答没有全对，可能的原因：
#  1. 基金股票持仓明细、基金可转债持仓明细 等表的日期不对