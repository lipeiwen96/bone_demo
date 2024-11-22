import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

# 加载 .env 文件中的环境变量
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('BASE_URL')
client = OpenAI(api_key=api_key, base_url=base_url)


def get_completion(input_message, model="gpt-3.5-turbo"):
    prompt = get_prompt(input_message)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "你是一个专业的骨代谢医生。"},
                  {"role": "user", "content": prompt}],
        temperature=0,  # 确保结果稳定
    )

    ai_output = response.choices[0].message.content

    try:
        # 清理可能的 Markdown 格式符号
        cleaned_output = clean_markdown_json(ai_output)
        result = json.loads(cleaned_output)
        return result
    except json.JSONDecodeError:
        raise ValueError(f"AI 返回结果无法解析为 JSON：\n{ai_output}")


def clean_markdown_json(raw_text):
    """
    清理 AI 返回的可能包含 Markdown 标记的 JSON 内容。
    """
    # 移除可能的 Markdown 代码块标记，例如 ```json 和 ```
    cleaned_text = re.sub(r"```json|```", "", raw_text).strip()
    return cleaned_text


def get_prompt(input_message):
    example_output = {
        "结论解读": "根据多项指标结果，患者的骨代谢状态总体表现为高动力性倾向。β-CTX指标显示骨吸收活性显著增强，提示骨量流失风险较高；P1NP指标处于正常范围，说明骨形成能力未见明显异常；维生素D水平不足可能影响钙吸收及骨代谢平衡；N-MID指标偏低，提示轻微骨形成不足。结合骨密度T值为正常，无明显骨质疏松风险。",
        "用药建议": "1. 补充钙剂（如碳酸钙）每日1000mg和维生素D 800-1200 IU；\n2. 若骨吸收过高，建议使用抗骨吸收药物如双膦酸盐或地舒单抗；\n3. 若进一步检查发现骨形成能力下降，可考虑使用特立帕肽以促进成骨。",
        "生活方式建议": "1. 增加户外活动，保证每日15-30分钟的阳光照射；\n2. 饮食中增加富含钙质和维生素D的食物，如奶制品、鱼类、鸡蛋等；\n3. 避免久坐、吸烟和过量饮酒，保持适度运动，建议进行低冲击力的抗阻运动如快走或瑜伽；\n4. 定期监测骨健康状况，避免跌倒等骨折风险。",
        "参考依据": "1. 《中国骨质疏松诊治指南（2020年版）》；\n2. 《骨转换生化标志物临床应用指南（2021）》；\n3. 《原发性骨质疏松症诊疗指南（2022）》。",
        "复诊建议": "建议3个月后复查骨代谢相关指标（如β-CTX、P1NP、N-MID）以及骨密度T值，评估干预效果。若骨代谢异常持续，应进一步排查继发性骨质疏松的潜在原因（如甲状旁腺功能亢进或维生素D缺乏）并调整治疗方案。"
    }

    prompt = f"""
    你是一名专业的骨代谢医生，根据以下输入数据生成综合分析报告：

    ### 输入数据说明
    - 患者的骨代谢检验数据包括以下指标：
        1. β-CTX (单位ng/ml)
        2. P1NP (单位μg/ml)
        3. VD (单位ng/ml)
        4. N-MID (单位ng/ml)
        5. PTH (单位ng/ml)
        6. CT (单位pg/ml)
        7. 骨密度T值 (可选)
    - 每个指标包含：当前值、参考区间、指标结果、指标解读、用药建议。

    ### 输出要求
    - 必须严格按照以下字段生成输出：
        1. 结论解读
        2. 用药建议
        3. 生活方式建议
        4. 参考依据
        5. 复诊建议
    - 输出格式为标准 JSON（Python 字典格式）。
    - 示例输出：{json.dumps(example_output, ensure_ascii=False, indent=2)}

    ### 输入数据
    {json.dumps(input_message, ensure_ascii=False, indent=2)}

    ### 请直接返回 JSON 格式的结果：
    """
    return prompt


if __name__ == "__main__":
    input_data = {
        "患者基本信息": {"性别": "男", "年龄": 50},
        "骨代谢检验数据": {
            "β-CTX": {"当前值": "1.0 ng/ml", "参考区间": "中偏高区间", "指标结果": "高动力型"},
            "P1NP": {"当前值": "30.0 μg/ml", "参考区间": "正常区间", "指标结果": "正常"}
        }
    }
    try:
        result = get_completion(input_data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(f"An error occurred: {e}")
