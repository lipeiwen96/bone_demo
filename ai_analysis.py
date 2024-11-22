"""
# 处理 input_data 的函数,调用各个分析模块并汇总
"""
from analysis_module.indicators_anlaysis import IndicatorsAnalysis
from analysis_module.ai_agent import get_completion


def ai_analysis(input_data, mode: str):
    """
    Processes the input data and validates it.

    Args:
        input_data (dict): Input data collected from the Streamlit interface.

    Returns:
        dict: A dictionary containing the status ("success" or "error") and a message.
    """
    try:
        # 校验必填字段
        required_biochemical_indicators = ["β-CTX", "P1NP", "25-Hydroxy Vitamin D", "N-MID Osteocalcin", "Parathyroid Hormone", "Calcitonin"]

        # 检查生化指标是否完整
        for field in required_biochemical_indicators:
            if not input_data["biochemical_indicators"].get(field):
                return {"status": "error", "message": f"Missing required biochemical indicator: {field}"}

        indicators_analysis = IndicatorsAnalysis(age=input_data["patient_info"]["age"])
        indicators_analysis.judge_is_male(input_data["patient_info"]["gender"])
        indicators_analysis.β_CTX.value = input_data["biochemical_indicators"]["β-CTX"]
        indicators_analysis.P1NP.value = input_data["biochemical_indicators"]["P1NP"]
        indicators_analysis.VD.value = input_data["biochemical_indicators"]["25-Hydroxy Vitamin D"]
        indicators_analysis.N_MID.value = input_data["biochemical_indicators"]["N-MID Osteocalcin"]
        indicators_analysis.PTH.value = input_data["biochemical_indicators"]["Parathyroid Hormone"]
        indicators_analysis.CT.value = input_data["biochemical_indicators"]["Calcitonin"]
        if input_data["imaging_data"]["Bone Density"] != "未输入":
            indicators_analysis.has_bone_density = True
            indicators_analysis.bone_density.value = input_data["imaging_data"]["Bone Density"]

        indicators_analysis.init()
        indicators_analysis.patient_indicators_log()
        indicators_analysis.analysis()

        # TODO： 接入大模型
        if mode == "slow":
            patient_basic_info = {
                "患者性别": input_data["patient_info"]["gender"],
                "患者年龄": input_data["patient_info"]["age"],
            }
            if input_data["patient_info"]["height"] > 100:
                patient_basic_info["患者身高"] = input_data["patient_info"]["height"]
            if input_data["patient_info"]["weight"] > 20:
                patient_basic_info["患者体重"] = input_data["patient_info"]["weight"]
            to_ai_json_input = {"患者基本信息": patient_basic_info,
                                "骨代谢检验数据": indicators_analysis.to_dict(containing_is_abnormal=False)}
            output = get_completion(to_ai_json_input, model="gpt-4o")
            print(output)

            result = {
                "指标逐一分析": indicators_analysis.to_dict(containing_is_abnormal=True),
                "综合分析及建议": output,
            }

            # TODO： 画图
            # TODO： 图传输？ streamlit自带图标功能

            return {"status": "success", "message": "Data processed successfully.", "result": result}
        else:
            result = {
                "指标逐一分析": indicators_analysis.to_dict(containing_is_abnormal=True),
            }
            return {"status": "success", "message": "Data processed successfully.", "result": result}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    input_data = {'patient_info':
                 {'gender': '男',
                       'age': 35,
                       'height': 0.0,
                       'weight': 0.0},
                  'biochemical_indicators':
                      {'β-CTX': 1.0,
                       'P1NP': 33.0,
                       '25-Hydroxy Vitamin D': 20.0,
                       'N-MID Osteocalcin': 15.0,
                       'Parathyroid Hormone': 27.0,
                       'Calcitonin': 1.0},
                  'imaging_data':
                      {'Bone Density': -1.0},
                  'medical_history':
                      {'history': '', 'medications': '', 'testing_time': ''}
                  }
    print(ai_analysis(input_data))

