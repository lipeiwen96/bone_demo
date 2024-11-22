"""
指标数据结构
"""
from dataclasses import field, dataclass
from typing import List


@dataclass
class SingleIndicator:
    # 输入
    name: str = field(default="")
    value: float = field(default=float)
    unit: str = field(default="")

    # 输出
    range: str = field(default="")  # 当前指标状态，“低”、“中”、“高”
    result: str = field(default="")  # 当前指标导向的结果类型：“低动力型”
    is_abnormal: bool = field(default=False)  # 指标结果是否异常，用于控制结果卡片的色板

    interpretation: str = field(default="")  # 对当前指标的医学解读
    guideline: str = field(default="")  # 参考依据或权威指南
    medication_suggestion: str = field(default="")  # 用药建议，如推荐药物类型
    lifestyle_suggestion: str = field(default="")  # 生活方式建议，如补钙、运动等

    reference_age_range: str = field(default="")  # 符合的年龄参考区间
    reference_value_range: str = field(default="")

    @property
    def log(self):
        return f"""
        指标数值: {self.value}, 对应区间: {self.range}, 对应类型: {self.result};
        医学解读: {self.interpretation}, 用药建议: {self.medication_suggestion}
        """

    def to_dict(self, containing_is_abnormal: bool = False):
        if containing_is_abnormal:
            return {
                "标题": f"{self.name} 指标解读",
                "当前值": f"{self.value} {self.unit}",
                "参考区间": f"{self.range}区间 {self.reference_value_range}",
                "指标结果": self.result,
                "指标解读": self.interpretation,
                "用药建议": self.medication_suggestion,
                "参考文件": self.guideline,
                "是否异常": self.is_abnormal,
            }
        else:
            return {
                "标题": f"{self.name} 指标解读",
                "当前值": f"{self.value} {self.unit}",
                "参考区间": f"{self.range}区间 {self.reference_value_range}",
                "指标结果": self.result,
                "指标解读": self.interpretation,
                "用药建议": self.medication_suggestion,
                "参考文件": self.guideline,
            }

