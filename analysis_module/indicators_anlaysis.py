"""
根据厂家提供的计算规则编写
"""
from dataclasses import field, dataclass
from typing import List
from analysis_module.single_indicator import SingleIndicator


@dataclass
class IndicatorsAnalysis:
    is_male: bool = field(default=True)
    age: int = field(default=0)  # 年龄，有可能没有
    β_CTX: SingleIndicator = field(default_factory=SingleIndicator)
    P1NP: SingleIndicator = field(default_factory=SingleIndicator)
    VD: SingleIndicator = field(default_factory=SingleIndicator)
    N_MID: SingleIndicator = field(default_factory=SingleIndicator)
    PTH: SingleIndicator = field(default_factory=SingleIndicator)
    CT: SingleIndicator = field(default_factory=SingleIndicator)
    has_bone_density: bool = field(default=False)
    bone_density: SingleIndicator = field(default_factory=SingleIndicator)

    def judge_is_male(self, input_gender: str):
        if input_gender == "男":
            self.is_male = True
        else:
            self.is_male = False

    def init(self):
        all_ranges = {
            "β_CTX_analysis": (0.0, 4.0),
            "P1NP_analysis": (10.0, 90.0),
            "VD_analysis": (0.0, 100.0),
            "N_MID_analysis": (0.0, 200.0),
            "PTH_analysis": (0.0, 100.0),
            "CT_analysis": (0.0, 40.0),
            "Bone_analysis": (-5.0, 5.0),
        }
        self.β_CTX.name = "β-胶原特殊序列(β-ctx)"
        self.β_CTX.unit = "ng/ml"
        self.β_CTX.reference_value_range_min, self.β_CTX.reference_value_range_max = all_ranges["β_CTX_analysis"]
        self.β_CTX.standard_value_range_min, self.β_CTX.standard_value_range_max = all_ranges["β_CTX_analysis"]
        self.P1NP.name = "总I型胶原氨基端延长肽(P1NP)"
        self.P1NP.unit = "μg/ml"
        self.P1NP.reference_value_range_min, self.P1NP.reference_value_range_max = all_ranges["P1NP_analysis"]
        self.P1NP.standard_value_range_min, self.P1NP.standard_value_range_max = all_ranges["P1NP_analysis"]
        self.VD.name = "25-羟基维生素D(VD)"
        self.VD.unit = "ng/ml"
        self.VD.reference_value_range_min, self.VD.reference_value_range_max = all_ranges["VD_analysis"]
        self.VD.standard_value_range_min, self.VD.standard_value_range_max = all_ranges["VD_analysis"]
        self.N_MID.name = "N端中段骨钙素(N-MID)"
        self.N_MID.unit = "ng/ml"
        self.N_MID.reference_value_range_min, self.N_MID.reference_value_range_max = all_ranges["N_MID_analysis"]
        self.N_MID.standard_value_range_min, self.N_MID.standard_value_range_max = all_ranges["N_MID_analysis"]
        self.PTH.name = "甲状旁腺激素(PTH)"
        self.PTH.unit = "ng/ml"
        self.PTH.reference_value_range_min, self.PTH.reference_value_range_max = all_ranges["PTH_analysis"]
        self.PTH.standard_value_range_min, self.PTH.standard_value_range_max = all_ranges["PTH_analysis"]
        self.CT.name = "降钙素(CT)"
        self.CT.unit = "pg/ml"
        self.CT.reference_value_range_min, self.CT.reference_value_range_max = all_ranges["CT_analysis"]
        self.CT.standard_value_range_min, self.CT.standard_value_range_max = all_ranges["CT_analysis"]
        self.bone_density.name = "骨密度T值"
        self.bone_density.unit = ""
        self.bone_density.reference_value_range_min, self.bone_density.reference_value_range_max = all_ranges["Bone_analysis"]
        self.bone_density.standard_value_range_min, self.bone_density.standard_value_range_max = all_ranges["Bone_analysis"]

    def patient_indicators_log(self):
        info = f"""
        ===== Patient Indicators Analysis =====
        性别: {'男性' if self.is_male else '女性'}，年龄: {self.age if self.age > 0 else '缺失年龄信息'}
        β-CTX (β-胶原特殊序列): {self.β_CTX.value} ng/ml
        P1NP (总I型胶原氨基端延长肽): {self.P1NP.value} μg/ml
        25-Hydroxy Vitamin D (25-羟基维生素D): {self.VD.value} ng/ml
        N-MID Osteocalcin (N-MID骨钙素): {self.N_MID.value} ng/ml
        Parathyroid Hormone (甲状旁腺素): {self.PTH.value} ng/ml
        Calcitonin (降钙素): {self.CT.value} pg/ml
        {f'Bone Density (骨密度): {self.bone_density.value} T-score' if self.has_bone_density else '无骨密度数值'}
        =====================================
        """
        print(info)

    def analysis(self):
        """执行所有指标的计算"""
        self.compute_β_CTX()
        self.compute_P1NP()
        self.compute_VD()
        self.compute_N_MID()
        self.compute_PTH()
        self.compute_CT()
        if self.has_bone_density:
            self.compute_bone_density()

        # TODO
        # 所有指标数据的汇总

    def compute_β_CTX(self):
        """计算 β-CTX 的区间和解读"""
        # 正常区间
        self.β_CTX.standard_value_range_min, self.β_CTX.standard_value_range_max = 0.3, 2.0
        self.β_CTX.interpretation = "β-CTX指标反映骨吸收活性。"
        if self.β_CTX.value < 0.2:
            self.β_CTX.range = "低"
            self.β_CTX.result = "低动力型"
            self.β_CTX.reference_value_range = f"β < 0.2{self.β_CTX.unit}"
            self.β_CTX.reference_value_range_min, self.β_CTX.reference_value_range_max = 0, 0.2
            self.β_CTX.interpretation += (
                f"当前指标处于低区间：{self.β_CTX.reference_value_range}。"
                f"骨吸收显著降低，破骨细胞活性不足，若骨密度 (T值) 低于-2.5，则为低动力型骨质疏松。常见于老年人、长期卧床或服用特定药物（如糖皮质激素）的患者。需要促进骨形成，而非抑制骨吸收。"
            )
            self.β_CTX.is_abnormal = True  # 标记为异常
            self.β_CTX.medication_suggestion = "成骨治疗：使用特立帕肽。"
        elif 0.2 <= self.β_CTX.value < 0.3:
            self.β_CTX.range = "中偏低"
            self.β_CTX.result = "中低型"
            self.β_CTX.reference_value_range_min, self.β_CTX.reference_value_range_max = 0.2, 0.3
            self.β_CTX.reference_value_range = f"0.2 < β < 0.3{self.β_CTX.unit}"
            self.β_CTX.interpretation += f"当前指标处于{'男性' if self.is_male else '女性'}的中低区间：{self.β_CTX.reference_value_range}。" \
                                         f"骨吸收略有活跃，但仍处于低水平，骨质流失较缓慢。若骨密度 (T值) 低于-2.5，则为早期骨质疏松，需要进行基础干预和补充治疗。"
            self.β_CTX.is_abnormal = True  # 标记为异常
            self.β_CTX.medication_suggestion = "服钙剂、维生素D。"
        elif 0.3 <= self.β_CTX.value < 2.0:
            threshold_value = 0.573
            if self.is_male:
                # 年龄判断模式
                if self.age < 50:
                    self.β_CTX.reference_age_range = "50岁以下"
                elif 50 <= self.age <= 70:
                    threshold_value = 0.695
                    self.β_CTX.reference_age_range = "50~70岁之间"
                else:
                    threshold_value = 0.835
                    self.β_CTX.reference_age_range = "70岁以上"
            else:
                # 女性
                threshold_value = 0.563

            if 0.3 <= self.β_CTX.value < threshold_value:
                self.β_CTX.range = "中"
                self.β_CTX.result = "中高动力型"
                self.β_CTX.reference_value_range = f"0.3 < β < {threshold_value}{self.β_CTX.unit}"
                self.β_CTX.reference_value_range_min, self.β_CTX.reference_value_range_max = 0.3, threshold_value
                if self.is_male:
                    self.β_CTX.interpretation += f"当前指标处于{self.β_CTX.reference_age_range}男性的中区间：{self.β_CTX.reference_value_range}。" \
                                                 f"骨吸收活性增强，若骨密度 (T值) 低于-2.5，则为中高动力型骨质疏松；" \
                                                 f"多见于围绝经期女性或老年人。需要积极控制骨吸收，防止骨量进一步流失。"
                else:
                    self.β_CTX.interpretation += f"当前指标处于女性的中区间：{self.β_CTX.reference_value_range}。" \
                                                 f"骨吸收活性增强，若骨密度 (T值) 低于-2.5，则为中高动力型骨质疏松；" \
                                                 f"多见于围绝经期女性或老年人。需要积极控制骨吸收，防止骨量进一步流失。"

                self.β_CTX.medication_suggestion = "抗骨治疗：双膦酸盐、地舒单抗"
            elif threshold_value <= self.β_CTX.value < 2.0:
                self.β_CTX.range = "中偏高"
                self.β_CTX.result = "高动力型（原发性）"
                self.β_CTX.reference_value_range_min, self.β_CTX.reference_value_range_max = threshold_value, 2.0
                self.β_CTX.reference_value_range = f"{threshold_value} < β < 2.0{self.β_CTX.unit}"
                if self.is_male:
                    self.β_CTX.interpretation += f"当前指标处于{self.β_CTX.reference_age_range}男性的中高区间：{self.β_CTX.reference_value_range}。" \
                                                 f"骨吸收显著活跃，骨代谢处于高动力状态，若骨密度 (T值) 低于-2.5，则为高动力型（原发性）骨质疏松。" \
                                                 f"骨量快速流失，易发生骨折，需要加强抗骨吸收治疗。"
                else:
                    self.β_CTX.interpretation += f"当前指标处于女性的中高区间：{self.β_CTX.reference_value_range}。" \
                                                 f"骨吸收活性增强，属于中高动力型骨质疏松；多见于围绝经期女性或老年人。需要积极控制骨吸收，防止骨量进一步流失。"
                self.β_CTX.medication_suggestion = "抗骨治疗：双膦酸盐、地舒单抗"
        else:
            self.β_CTX.range = "高"
            self.β_CTX.result = "高动力型（继发性）"
            self.β_CTX.is_abnormal = True  # 标记为异常
            self.β_CTX.reference_value_range = f"β ≥ 2.0{self.β_CTX.unit}（约两倍参考值）"
            self.β_CTX.reference_value_range_min = 2.0
            self.β_CTX.interpretation += f"当前指标处于高区间：{self.β_CTX.reference_value_range}。" \
                                         f"骨吸收极为活跃，属于高动力型（继发性）骨质疏松，通常由 继发性病因（如甲状旁腺功能亢进）导致，病因明确的情况下，应先解决基础问题，再进行骨质疏松治疗。"
            self.β_CTX.medication_suggestion = "抗骨治疗：双膦酸盐、地舒单抗"

        # TODO: 参考依据随便写的
        self.β_CTX.guideline = "原发性骨质疏松症诊疗指南_2022.pdf、中国老年骨质疏松症诊疗指南（2023）.pdf"

    def compute_P1NP(self):
        """计算 P1NP 的区间和解读"""
        self.P1NP.interpretation = "P1NP指标是骨形成标志物，反映成骨细胞活性。"

        # 正常区间
        self.P1NP.standard_value_range_min, self.P1NP.standard_value_range_max = 22.59, 75.17

        threshold_low = 14.56
        threshold_high = 59.62
        if self.is_male:
            threshold_low = 22.59
            threshold_high = 75.17
        else:
            pass

        if self.P1NP.value < threshold_low:
            self.P1NP.range = "低"
            self.P1NP.result = "低动力型"
            self.P1NP.is_abnormal = True  # 标记为异常
            self.P1NP.reference_value_range = f"P1NP < {threshold_low}{self.P1NP.unit}"
            self.P1NP.reference_value_range_max = threshold_low
            self.P1NP.interpretation += f"当前指标处于{'男性' if self.is_male else '女性'}的低区间：{self.β_CTX.reference_value_range}。" \
                                        f"提示骨形成能力下降，若骨密度 (T值) 低于-2.5，则为低动力型骨质疏松。成骨细胞活性不足，骨代谢失衡，易导致骨量丢失和脆性骨折。" \
                                        f"常见于老年患者、长期使用糖皮质激素或其他影响骨形成的慢性疾病。"
            self.P1NP.medication_suggestion = "成骨治疗：特立帕肽"
        elif threshold_low <= self.P1NP.value < threshold_high:
            self.P1NP.range = "中"
            self.P1NP.reference_value_range = f"{threshold_low} <= P1NP < {threshold_high}{self.P1NP.unit}"
            self.P1NP.reference_value_range_min, self.P1NP.reference_value_range_max = threshold_low, threshold_high
            self.P1NP.interpretation += f"当前指标处于{'男性' if self.is_male else '女性'}的正常区间：{self.β_CTX.reference_value_range}。" \
                                        f"说明骨吸收与骨形成处于平衡状态，无明显骨代谢异常。正常骨代谢患者无需特殊治疗，但若存在骨密度下降趋势或骨折风险，则需采取预防措施。"
            self.P1NP.result = "正常"
        else:
            self.P1NP.range = "高"
            self.P1NP.result = "重度骨量流失"
            self.P1NP.is_abnormal = True  # 标记为异常
            self.P1NP.reference_value_range = f"P1NP >= {threshold_high}{self.P1NP.unit}（参考值范围浮动）"
            self.P1NP.reference_value_range_min = threshold_high
            self.P1NP.interpretation += f"当前指标处于{'男性' if self.is_male else '女性'}的高区间：{self.β_CTX.reference_value_range}。" \
                                        f"骨形成活跃，但常伴随骨吸收增加，提示高转换状态、重度骨量流失。" \
                                        f"需综合评估 β-CTX 和 PTH指标，明确是否存在继发性骨质疏松。"
            self.P1NP.medication_suggestion = "抗骨治疗：双膦酸盐或者地舒单抗"

        # TODO: 参考依据随便写的
        self.P1NP.guideline = "总I型胶原氨基端延长肽（Total-P1NP）.pdf"

    def compute_VD(self):
        """计算 25-羟基维生素D 的区间和解读"""
        # 正常区间
        self.VD.standard_value_range_min, self.VD.standard_value_range_max = 20, 30
        if self.VD.value < 20:
            self.VD.range = "严重不足"
            self.VD.is_abnormal = True  # 标记为异常
            self.VD.reference_value_range = f"VD < 20{self.VD.unit}"
            self.VD.reference_value_range_max = 20
            self.VD.result = "维生素D缺乏"
            self.VD.interpretation += f"维生素D严重不足，可能导致钙吸收降低，引发骨质疏松、骨软化甚至低钙血症。" \
                                        f"老年人、孕妇、长期日照不足者或肝肾功能不全患者常见。需快速补充维生素D，避免进一步骨质流失或并发症。"
        elif 20 <= self.VD.value < 30:
            self.VD.range = "低"
            self.VD.reference_value_range = f"20 ≤ VD < 30{self.VD.unit}"
            self.VD.reference_value_range_min, self.VD.reference_value_range_max = 20, 30
            self.VD.result = "维生素D不足"
            self.VD.interpretation += f"维生素D水平低于理想范围，但尚未导致严重代谢紊乱。钙吸收率下降，可能存在轻度骨质减少，长期维持此状态会增加骨质疏松风险。"
        else:
            self.VD.range = "正常"
            self.VD.reference_value_range = f"VD ≥ 30{self.VD.unit}"
            self.VD.reference_value_range_min = 30
            self.VD.result = "维生素D充足"
            self.VD.interpretation += f"维生素D水平在理想范围内，钙吸收效率高，骨代谢处于正常状态。"

        self.VD.guideline = "25-羟基维生素D（25-Hydroxyvitamin D）.pdf、《骨转换生化标志物临床应用指南》2021版.pdf"

    def compute_N_MID(self):
        """计算 N-MID 骨钙素"""
        self.N_MID.interpretation = "N-MID指标反映成骨细胞功能水平, 在血液中相比骨钙素更稳定。"

        threshold_low = 22
        threshold_high = 69
        reference_age_range = ""
        reference_age_range = ""
        if self.age <= 29:
            # 参考范围为 22-69
            self.N_MID.reference_age_range = "18~29岁"
            self.N_MID.reference_value_range = "22 < N-MID < 69ng/ml"
            # 正常区间
            self.N_MID.standard_value_range_min, self.N_MID.standard_value_range_max = 14.8, 64.5
        elif 29 < self.age <= 50:
            # 参考范围为 15-41
            threshold_low = 22
            threshold_high = 69
            self.N_MID.reference_age_range = "30~50岁"
            self.N_MID.reference_value_range = "15 < N-MID < 41ng/ml"
            # 正常区间
            self.N_MID.standard_value_range_min, self.N_MID.standard_value_range_max = 15, 41
        elif 50 < self.age <= 70:
            # 参考范围为 15-41
            threshold_low = 15
            threshold_high = 46
            self.N_MID.reference_age_range = "51~70岁"
            self.N_MID.reference_value_range = "15 < N-MID < 46ng/ml"
            # 正常区间
            self.N_MID.standard_value_range_min, self.N_MID.standard_value_range_max = 15, 46
        else:
            # 老年人
            threshold_low = threshold_high = 13
            self.N_MID.reference_age_range = "70岁以上"
            self.N_MID.reference_value_range = "N-MID  < 13g/ml"
            self.N_MID.standard_value_range_max = 13

        if self.N_MID.value < threshold_low:
            self.N_MID.reference_value_range_max = threshold_low
            self.N_MID.range = "低"
            if self.has_bone_density:
                if self.bone_density.value < -2.5:
                    self.N_MID.is_abnormal = True  # 标记为异常
                    self.N_MID.result = "骨形成不足或低动力型骨质疏松(缺失材料)"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; 当前N-MID数值低于区间。" \
                                                f"结合骨密度 (T值) 低于-2.5，推测为骨形成不足或低动力型骨质疏松，需重点促进骨形成。"
                else:
                    self.N_MID.result = "轻微骨形成不足(缺失材料)"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; 当前N-MID数值低于区间。" \
                                                f"但骨密度 (T值) 数值正常, 提示可能存在轻微骨形成不足，但无明显骨质疏松风险。建议定期复查骨密度并关注骨健康。"
            else:
                self.N_MID.is_abnormal = True  # 标记为异常
                self.N_MID.result = "骨形成不足(缺失材料)"
                self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                            f"为{self.N_MID.reference_value_range}; 当前N-MID数值低于区间。" \
                                            f"建议进一步评估骨密度情况，结合骨密度T值综合判断。"

        elif threshold_low <= self.N_MID.value <= threshold_high * 2:
            self.N_MID.standard_value_range_min, self.N_MID.standard_value_range_max = threshold_low, threshold_high * 2
            self.N_MID.range = "正常"
            if self.has_bone_density:
                if self.bone_density.value < -2.5:
                    self.N_MID.is_abnormal = True  # 标记为异常
                    self.N_MID.result = "低动力型骨质疏松"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; " \
                                                f"{'当前N-MID数值正常' if self.N_MID.value <= threshold_high else '当前N-MID数值偏高'}。" \
                                                f"结合骨密度 (T值) 低于-2.5，推测为原发性骨质疏松，需重点促进骨形成。需关注骨质疏松风险。"
                else:
                    self.N_MID.result = "正常"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; " \
                                                f"{'当前N-MID数值正常' if self.N_MID.value <= threshold_high else '当前N-MID数值偏高'}。" \
                                                f"结合骨密度 (T值) 正常，说明骨代谢处于平衡状态，无明显骨代谢异常。"
            else:
                if self.N_MID.value <= threshold_high:
                    self.N_MID.result = "正常"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; " \
                                                f"当前N-MID数值偏高。" \
                                                f"由于未提供骨密度T值数据，建议结合影像学评估进一步确认骨质健康情况。"
                else:
                    self.N_MID.is_abnormal = True  # 标记为异常
                    self.N_MID.result = "骨代谢活跃"
                    self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                                f"为{self.N_MID.reference_value_range}; " \
                                                f"当前N-MID数值偏高。" \
                                                f"可能提示骨代谢活跃状态，建议结合骨密度T值和临床表现进一步评估。尤其需关注是否存在骨吸收增加导致的骨量减少风险。"

        else:
            self.N_MID.standard_value_range_min = threshold_high * 2
            self.N_MID.is_abnormal = True  # 标记为异常
            self.N_MID.range = "高"
            self.N_MID.result = "继发性骨质疏松"
            self.N_MID.interpretation = f"对于{self.N_MID.reference_age_range}年龄群体的N-MID参考范围" \
                                        f"为{self.N_MID.reference_value_range}; N-MID数值超出参考范围两倍，严重偏高。" \
                                        f"推测为继发性骨质疏松，可能与肾功能不全、甲状旁腺功能异常、恶性肿瘤等继发性因素相关。" \
                                        f"建议患者去肾内科评估肾功能（GFR 检查），必要时治疗基础病因，骨代谢干预需谨慎。"
        self.N_MID.guideline = "N-MID骨钙素（N-MID Osteocalcin）.pdf、原发性骨质疏松症诊疗指南_2022.pdf"

    def compute_PTH(self):
        """计算 PTH 的区间和解读"""
        # 正常区间
        self.PTH.standard_value_range_min, self.PTH.standard_value_range_max = 14.8, 64.5
        if self.PTH.value < 14.8:
            self.PTH.range = "低"
            self.PTH.reference_value_range = f"PTH < 14.8{self.VD.unit}"
            self.PTH.reference_value_range_max = 14.8
            self.PTH.is_abnormal = True  # 标记为异常
            if self.has_bone_density:
                if self.bone_density.value < -2.5:
                    self.PTH.result = "非甲旁引起的骨质疏松症"
                    self.PTH.interpretation += (
                        f"当前指标处于低区间：{self.PTH.reference_value_range}。结合骨密度 (T值) 低于-2.5，提示骨质疏松可能由其他非甲状旁腺原因引起，"
                        f"如营养不良或维生素D缺乏。建议进一步评估其他骨代谢相关因素。"
                    )
                else:
                    self.PTH.result = "非甲旁引起的轻微骨质疏松风险"
                    self.PTH.interpretation += (
                        f"当前指标处于低区间：{self.PTH.reference_value_range}，但骨密度 (T值) 正常。提示甲状旁腺功能可能正常，但需注意是否存在轻微骨形成不足或其他骨健康问题。"
                    )
            else:
                self.PTH.result = "非甲旁相关骨代谢异常"
                self.PTH.interpretation += (
                    f"当前指标处于低区间：{self.PTH.reference_value_range}。未提供骨密度 (T值) 数据，建议结合骨密度检查进一步评估是否存在骨质疏松或其他代谢异常。"
                )
        elif 14.8 <= self.PTH.value <= 64.5:
            self.PTH.range = "正常"
            self.PTH.reference_value_range = f"14.8 ≤ PTH ≤ 64.5{self.VD.unit}"
            self.PTH.reference_value_range_min, self.PTH.reference_value_range_max = 14.8, 64.5
            if self.has_bone_density:
                if self.bone_density.value < -2.5:
                    self.PTH.is_abnormal = True  # 标记为异常
                    self.PTH.result = "非甲旁引起的骨质疏松症"
                    self.PTH.interpretation += (
                        f"当前指标处于正常区间：{self.PTH.reference_value_range}。但骨密度 (T值) 低于-2.5，提示骨质疏松可能由其他因素引起，如骨吸收过高或骨形成不足。"
                    )
                else:
                    self.PTH.result = "正常骨代谢"
                    self.PTH.interpretation += (
                        f"当前指标处于正常区间：{self.PTH.reference_value_range}。且骨密度 (T值) 正常。说明甲状旁腺功能正常，骨代谢无明显异常。"
                    )
            else:
                self.PTH.result = "正常骨代谢"
                self.PTH.interpretation += (
                    f"当前指标处于正常区间：{self.PTH.reference_value_range}。未提供骨密度 (T值) 数据，建议结合影像学检查进一步确认骨健康状态。"
                )
        else:
            self.PTH.range = "偏高"
            self.PTH.is_abnormal = True  # 标记为异常
            self.PTH.reference_value_range = f"PTH > 64.5{self.VD.unit}"
            self.PTH.reference_value_range_min = 64.5
            if self.has_bone_density:
                if self.bone_density.value < -2.5:
                    self.PTH.result = "甲旁亢引起的骨质疏松症"
                    self.PTH.interpretation += (
                        f"当前指标处于偏高区间：{self.PTH.reference_value_range}。结合骨密度 (T值) 低于-2.5，提示甲状旁腺功能亢进导致的骨吸收过高，可能伴随骨质疏松症风险。"
                        f"建议进行甲状旁腺功能检查，评估是否存在甲旁亢或继发性骨质疏松。"
                    )
                else:
                    self.PTH.result = "甲旁亢导致的骨代谢异常"
                    self.PTH.interpretation += (
                        f"当前指标处于偏高区间：{self.PTH.reference_value_range}。"
                        f"但骨密度 (T值) 正常。提示甲状旁腺功能亢进，但尚未引发明显骨量减少。建议监测甲状旁腺功能和骨密度变化。"
                    )
            else:
                self.PTH.result = "甲旁相关异常"
                self.PTH.interpretation += (
                    f"当前指标处于偏高区间：{self.PTH.reference_value_range}。未提供骨密度 (T值) 数据，建议进行甲状旁腺功能检查，结合影像学评估进一步确认骨健康状态。"
                )
        # 添加参考文件
        self.PTH.guideline = "原发性骨质疏松症诊疗指南_2022.pdf"

    def compute_CT(self):
        """计算降钙素的区间和解读"""
        threshold_value = 6.26
        if self.is_male:
            threshold_value = 9.72
        else:
            pass
        # 正常区间
        self.CT.standard_value_range_max = threshold_value

        if self.CT.value < threshold_value:
            self.CT.range = "正常"
            self.CT.reference_value_range = f"CT ≤ {9.72 if self.is_male else 6.26}{self.VD.unit}"
            self.CT.reference_value_range_max = threshold_value
            self.CT.result = "正常"
            self.CT.interpretation = f"{'男性' if self.is_male else '女性'}正常区间为CT值 ≤ {threshold_value}pg/ml，" \
                                      f"当前指标正常。提示骨代谢活动无明显异常，患者的骨吸收状态良好。" \
                                      f"骨质疏松风险可能不由甲状腺髓样瘤、肺小细胞癌等疾病引起。"
        else:
            self.CT.is_abnormal = True  # 标记为异常
            self.CT.range = "偏高"
            self.CT.reference_value_range = f"CT ≥ {9.72 if self.is_male else 6.26}{self.VD.unit}"
            self.bone_density.reference_value_range_min = threshold_value
            self.CT.result = "提示甲状腺髓样瘤"
            self.CT.interpretation = f"{'男性' if self.is_male else '女性'}正常区间为CT值 ≤ {threshold_value}pg/ml，" \
                                      f"当前指标显著偏高，（尤其是CT值升高超过参考值上限的两倍以上），需结合患者病史、影像学检查和甲状腺功能评估，" \
                                      f"明确是否存在甲状腺髓样癌、肺小细胞癌或其他肿瘤性疾病。要与患者的骨代谢问题（如骨质疏松或高骨吸收状态）区分开来。"

        self.CT.guideline = "骨质疏松性骨折诊疗指南（2022年版）.pdf、中国老年骨质疏松症诊疗指南（2023）.pdf"

    def compute_bone_density(self):
        """计算骨密度"""
        self.bone_density.interpretation = "骨密度（T值）是骨量的重要指标，用于评估骨质疏松风险。"
        # 正常区间
        self.bone_density.standard_value_range_min, self.bone_density.standard_value_range_max = -1.0, 1.0

        if self.bone_density.value >= -1.0:
            self.bone_density.range = "正常"
            self.bone_density.reference_value_range = f"T值 ≥ -1.0"
            self.bone_density.reference_value_range_min = -1.0
            self.bone_density.result = "骨密度正常"
            self.bone_density.interpretation += (
                f"当前骨密度T值为{self.bone_density.value}，处于正常范围：{self.CT.reference_value_range}。"
                f"提示骨量良好，骨折风险较低，无需特别干预，但建议定期监测骨密度变化。"
            )
        elif -2.5 < self.bone_density.value < -1.0:
            self.bone_density.range = "偏低"
            self.bone_density.reference_value_range = f"-2.5 < T值 < -1.0"
            self.bone_density.reference_value_range_min, self.bone_density.reference_value_range_max = -2.5, -1.0
            self.bone_density.result = "骨量减少"
            self.bone_density.interpretation += (
                f"当前骨密度T值为{self.bone_density.value}，处于骨量减少范围：{self.CT.reference_value_range}。"
                f"提示骨量低于正常水平，但尚未达到骨质疏松的诊断标准。"
                f"建议适当补充钙和维生素D，保持运动，预防进一步骨量丢失。"
            )
        else:
            self.bone_density.is_abnormal = True  # 标记为异常
            self.bone_density.range = "过低"
            self.bone_density.reference_value_range = f"T值 ≤ -2.5"
            self.bone_density.reference_value_range_max = -2.5
            self.bone_density.result = "骨质疏松"
            self.bone_density.interpretation += (
                f"当前骨密度T值为{self.bone_density.value}，低于骨质疏松诊断标准：{self.CT.reference_value_range}。"
                f"提示骨量显著减少，骨折风险显著增加。"
                f"建议进行药物干预（如抗骨吸收治疗），同时补充钙和维生素D，必要时结合骨代谢指标综合评估治疗效果。"
            )

        self.bone_density.guideline = "《中国骨质疏松诊治指南（2020年版）》、DXA骨密度检测标准.pdf"

    def to_dict(self, containing_is_abnormal: bool = False):
        if self.has_bone_density:
            return {
                "β_CTX_analysis": self.β_CTX.to_dict(containing_is_abnormal),
                "P1NP_analysis": self.P1NP.to_dict(containing_is_abnormal),
                "VD_analysis": self.VD.to_dict(containing_is_abnormal),
                "N_MID_analysis": self.N_MID.to_dict(containing_is_abnormal),
                "PTH_analysis": self.PTH.to_dict(containing_is_abnormal),
                "CT_analysis": self.CT.to_dict(containing_is_abnormal),
                "Bone_analysis": self.bone_density.to_dict(containing_is_abnormal),
            }
        else:
            return{
                "β_CTX_analysis": self.β_CTX.to_dict(containing_is_abnormal),
                "P1NP_analysis": self.P1NP.to_dict(containing_is_abnormal),
                "VD_analysis": self.VD.to_dict(containing_is_abnormal),
                "N_MID_analysis": self.N_MID.to_dict(containing_is_abnormal),
                "PTH_analysis": self.PTH.to_dict(containing_is_abnormal),
                "CT_analysis": self.CT.to_dict(containing_is_abnormal),
            }


