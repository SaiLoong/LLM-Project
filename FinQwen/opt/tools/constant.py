# -*- coding: utf-8 -*-
# @file constant.py
# @author zhangshilong
# @date 2024/7/7

NA = "N/A"  # 载入csv时，会被pandas当成NaN处理


class Enum:
    @classmethod
    def items(cls):
        return {(k, v) for k, v in vars(cls).items()
                if not k.startswith("_") and not isinstance(v, (classmethod, list, set))}

    @classmethod
    def keys(cls):
        return {k for k, v in vars(cls).items()
                if not k.startswith("_") and not isinstance(v, (classmethod, list, set))}

    @classmethod
    def values(cls):
        return {v for k, v in vars(cls).items()
                if not k.startswith("_") and not isinstance(v, (classmethod, list, set))}


class ModelName(Enum):
    QWEN_1_8B_CHAT = "Qwen-1_8B-Chat"

    # TONGYI_FINANCE_14B_CHAT = "Tongyi-Finance-14B-Chat"
    TONGYI_FINANCE_14B_CHAT_INT4 = "Tongyi-Finance-14B-Chat-Int4"


class Label(Enum):
    TEXT = "Text"
    SQL = "SQL"


Category = Label


class ModelMode(Enum):
    TRAIN = "train"
    EVAL = "eval"
