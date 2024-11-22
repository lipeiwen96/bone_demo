import streamlit as st
import json
from ai_analysis import ai_analysis

# 定义用于存储每个指标分析结果的变量
β_CTX_analysis = ""
P1NP_analysis = ""
VD_analysis = ""
N_MID_analysis = ""
PTH_analysis = ""
CT_analysis = ""


if __name__ == "__main__":
    # 设置页面布局
    st.set_page_config(
        page_title="骨代谢AI智能检测",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # 页面标题
    st.title("Bone Metabolism AI | 骨代谢AI模型")
    # 添加简介区域
    st.markdown(
        """
        <div style="background-color: #f0f0f0; padding: 5px; border-radius: 2px;">
            <p style="font-size: 13px; color: #888;">研发团队：东莞康华医院检验科AI研发团队 | DEMO版本号：v0.0.1</p>
            <p style="font-size: 14px; color: #555;">
            🦴骨代谢指标智能分析AI模型，您可通过输入患者信息和生化指标，快速获得智能化的分析结果。
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")  # 上方分割线

    # 患者信息输入区
    st.markdown("### 患者信息")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("**性别（必须项）**", ["男", "女"]) #"请选择",
        height = st.number_input(":grey[身高（cm，可选项）]", min_value=0.0, max_value=250.0, step=0.1)
    with col2:
        age = st.number_input("**年龄（必须项）**", min_value=18, max_value=120, step=1, value=35)
        weight = st.number_input(":grey[体重（kg，可选项）]", min_value=0.0, max_value=200.0, step=0.1)
    # 既往病史输入区
    with st.expander("### 既往病史的补充信息（暂未接入，后续持续升级）"):
        history = st.text_area(":grey[既往病史（例如：脆性骨折、内分泌疾病、肾功能不全等，可选项）]")
        medications = st.text_area(":grey[用药史（例如：双膦酸盐、地舒单抗、特立帕肽等，可选项）]")
        testing_time = st.text_input(":grey[检测时间节点（例如：首次检测、随访复测，可选项）]")

    # 生化指标输入区
    st.markdown("### 生化指标")
    β_CTX = st.number_input(
        "**β-胶原特殊序列, β-CTX（ng/ml，必须项）**",
        min_value=0.0,
        max_value=5.0,  # 合理范围设为 0.0-2.5
        step=0.1,
        format="%.3f",  # 保留三位小数
        value=1.0,
        help="正常范围：0.1 - 2.0 ng/ml，高于 2.0 表示风险增高。"
    )

    P1NP = st.number_input(
        "**总I型胶原氨基端延长肽, P1NP（μg/ml，必须项）**",
        min_value=0.0,
        max_value=100.0,  # 根据数据设置宽泛范围
        step=0.1,
        format="%.2f",
        value=33.0,
        help="β-CTX反映骨吸收活性。正常范围：15 - 75 μg/ml，高于 75 μg/ml 可能提示骨质代谢异常。"
    )

    VD = st.number_input(
        "**25-羟基维生素D, VD（ng/ml，必须项）**",
        min_value=0.0,
        max_value=100.0,  # 宽泛合理范围
        step=0.1,
        format="%.1f",
        value=20.0,
        help="P1NP是骨形成标志物，反映成骨细胞活性。正常范围：20 - 50 ng/ml，低于 20 ng/ml 可能为维生素D缺乏。"
    )

    N_MID = st.number_input(
        "**N-MID骨钙素, N-MID（ng/ml，必须项）**",
        min_value=0.0,
        max_value=100.0,  # 宽泛合理范围
        step=0.1,
        format="%.1f",
        value=15.0,
        help="反映成骨细胞功能水平, 在血液中相比骨钙素更稳定。正常范围：15 - 50 ng/ml，超出范围可能提示代谢异常。"
    )

    PTH = st.number_input(
        "**甲状旁腺素, PTH（ng/ml，必须项）**",
        min_value=0.0,
        max_value=100.0,  # 根据图片数据合理推测
        step=0.1,
        format="%.2f",
        value=27.0,
        help="正常范围：15 - 65 ng/ml，高于 65 ng/ml 提示甲状旁腺功能亢进可能。"
    )

    CT = st.number_input(
        "**降钙素, CT（pg/ml，必须项）**",
        min_value=0.0,
        max_value=50.0,  # 根据图片及临床经验设置上限
        step=0.1,
        format="%.2f",
        value=1.0,
        help="正常范围：0 - 10 pg/ml，高于 10 pg/ml 提示相关甲状腺病变可能。"
    )

    # 影像学检查输入区
    # st.markdown("### 影像学检查数据（可选项）")
    use_bone_density = st.checkbox(":grey[是否输入骨密度T值？]")  # 添加复选框
    bone_density = st.number_input(
        ":grey[骨密度T值（例如：DXA或QCT，可选项）]",
        value=-1.0,
        min_value=-5.0,  # 设置最低值为 -5.0，超出实际骨密度范围的安全下限
        max_value=5.0,   # 设置最高值为 5.0，超出正常范围的安全上限
        step=0.1,        # 设置输入步长为 0.1，便于精确输入
        format="%.1f",   # 保留一位小数
        help="骨密度T值常见取值范围为 -5.0 到 5.0，正常范围为 ≥ -1.0"
    )

    st.markdown("---")  # 上方分割线

    # 创建两列用于放置按钮
    col1, col2, col3 = st.columns([3, 5, 5])  # 调整列的宽度比例，例如左1:中6:右1
    # 用于存储按钮的点击状态
    button1_clicked = False
    button2_clicked = False
    # 在第一列放置第一个按钮
    with col1:
        if st.button("🚀 指标极速分析"):
            button1_clicked = True
    # 在第二列放置第二个按钮
    with col2:
        if st.button("🧠 AI全面分析"):
            button2_clicked = True

    # AI 分析按钮

    if button1_clicked:
        # 验证必填项
        error_messages = []
        if gender == "请选择":
            error_messages.append("请在患者性别字段中选择一项。")
        if age <= 0:
            error_messages.append("请输入正确的患者年龄。")
        if β_CTX <= 0:
            error_messages.append("β-胶原特殊序列（ng/ml）必须输入大于0的值。")
        if P1NP <= 0:
            error_messages.append("总I型胶原氨基端延长肽（μg/ml）必须输入大于0的值。")
        if VD <= 0:
            error_messages.append("25-羟基维生素D（ng/ml）必须输入大于0的值。")
        if N_MID <= 0:
            error_messages.append("N-MID骨钙素（ng/ml）必须输入大于0的值。")
        if PTH <= 0:
            error_messages.append("甲状旁腺素（ng/ml）必须输入大于0的值。")
        if CT <= 0:
            error_messages.append("降钙素（pg/ml）必须输入大于0的值。")

        # 如果有错误，显示提示并返回
        if error_messages:
            for msg in error_messages:
                st.error(msg)
        else:
            # 组织输入数据
            input_data = {
                "patient_info": {
                    "gender": gender,
                    "age": age,
                    "height": height,
                    "weight": weight,
                },
                "biochemical_indicators": {
                    "β-CTX": β_CTX,
                    "P1NP": P1NP,
                    "25-Hydroxy Vitamin D": VD,
                    "N-MID Osteocalcin": N_MID,
                    "Parathyroid Hormone": PTH,
                    "Calcitonin": CT,
                },
                "imaging_data": {
                    "Bone Density": bone_density if use_bone_density else "未输入",
                },
                "medical_history": {
                    "history": history,
                    "medications": medications,
                    "testing_time": testing_time,
                },
            }

            print(input_data)

            # 调用AI分析函数
            result = ai_analysis(input_data, mode="fast")

            # 根据返回结果显示信息
            if result["status"] == "success":
                st.success("分析完成！以下为详细结果：")
                all_results = result.get("result", {})
                analysis_results = all_results.get("指标逐一分析", {})

                # 分块显示单一指标分析
                st.markdown("#### 指标逐一分析")
                # 定义卡片样式
                full_card_style = """
                <div style="background-color: {background_color}; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                    <h5 style="color: #333; margin-bottom: 10px;">{title}{abnormal_tag}</h5>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #555; margin-bottom: 10px;">
                        <span><strong>当前值：</strong>{current_value}</span>
                        <span><strong>指标区间：</strong>{range}</span>
                        <span><strong>指标结果：</strong>{result}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #555;">
                        <span><strong>指标解读：</strong>{interpretation}</span>
                        <span><strong>用药建议：</strong>{recommendation}</span>
                        <span><strong>参考文件(仅作示意)：</strong>{reference}</span>
                    </div>
                </div>
                """
                without_recommendation_card_style = """
                <div style="background-color: {background_color}; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                    <h5 style="color: #333; margin-bottom: 10px; ">{title}{abnormal_tag}</h5>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #555; margin-bottom: 10px;">
                        <span><strong>当前值：</strong>{current_value}</span>
                        <span><strong>指标区间：</strong>{range}</span>
                        <span><strong>指标结果：</strong>{result}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #555;">
                        <span><strong>指标解读：</strong>{interpretation}</span>
                        <span><strong>参考文件(仅作示意)：</strong>{reference}</span>
                    </div>
                </div>
                """

                for indicator, analysis in analysis_results.items():
                    # 判断是否异常并设置背景颜色
                    background_color = "#f9f9f9"  # 默认背景色
                    abnormal_tag = ""  # 默认没有异常提示
                    if analysis["是否异常"]:
                        background_color = "#ffe6e6"  # 浅红色背景
                        abnormal_tag = """<span style="background-color: #ff0000; color: #fff; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-left: 20px;">
                                          异常
                                          </span>"""

                    # 如果 interpretation 为空，则不渲染该字段
                    if analysis["用药建议"]:
                        st.markdown(
                            full_card_style.format(
                                background_color=background_color,
                                title=analysis["标题"],
                                abnormal_tag=abnormal_tag,
                                current_value=analysis["当前值"],
                                range=analysis["参考区间"],
                                result=analysis["指标结果"],
                                interpretation=analysis["指标解读"],
                                recommendation=analysis["用药建议"],
                                reference=analysis["参考文件"],
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            without_recommendation_card_style.format(
                                background_color=background_color,
                                title=analysis["标题"],
                                abnormal_tag=abnormal_tag,
                                current_value=analysis["当前值"],
                                range=analysis["参考区间"],
                                result=analysis["指标结果"],
                                interpretation=analysis["指标解读"],
                                reference=analysis["参考文件"],
                            ),
                            unsafe_allow_html=True,
                        )

                # 可视化展示
                st.markdown("#### 数据图表")
                st.text("正在进行中... 很快就来")
                # st.markdown("以下为患者各项指标的变化趋势和对比分析：")
                #
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.markdown("#### 当前指标变化趋势")
                #     # 绘制趋势折线图（示例）
                #     st.line_chart(analysis_results['trend_data'])
                # with col2:
                #     st.markdown("#### 全国数据对比")
                #     # 显示柱状图或分布图（示例）
                #     st.bar_chart(analysis_results['comparison_data'])

                # st.markdown("#### 骨密度变化对比")
                # 骨密度变化图（示例）
                # st.line_chart(analysis_results['bone_density_trend'])
            else:
                st.error(result["message"])

    if button2_clicked:
        # 验证必填项
        error_messages = []
        if gender == "请选择":
            error_messages.append("请在患者性别字段中选择一项。")
        if age <= 0:
            error_messages.append("请输入正确的患者年龄。")
        if β_CTX <= 0:
            error_messages.append("β-胶原特殊序列（ng/ml）必须输入大于0的值。")
        if P1NP <= 0:
            error_messages.append("总I型胶原氨基端延长肽（μg/ml）必须输入大于0的值。")
        if VD <= 0:
            error_messages.append("25-羟基维生素D（ng/ml）必须输入大于0的值。")
        if N_MID <= 0:
            error_messages.append("N-MID骨钙素（ng/ml）必须输入大于0的值。")
        if PTH <= 0:
            error_messages.append("甲状旁腺素（ng/ml）必须输入大于0的值。")
        if CT <= 0:
            error_messages.append("降钙素（pg/ml）必须输入大于0的值。")

        # 如果有错误，显示提示并返回
        if error_messages:
            for msg in error_messages:
                st.error(msg)
        else:
            # 组织输入数据
            input_data = {
                "patient_info": {
                    "gender": gender,
                    "age": age,
                    "height": height,
                    "weight": weight,
                },
                "biochemical_indicators": {
                    "β-CTX": β_CTX,
                    "P1NP": P1NP,
                    "25-Hydroxy Vitamin D": VD,
                    "N-MID Osteocalcin": N_MID,
                    "Parathyroid Hormone": PTH,
                    "Calcitonin": CT,
                },
                "imaging_data": {
                    "Bone Density": bone_density if use_bone_density else "未输入",
                },
                "medical_history": {
                    "history": history,
                    "medications": medications,
                    "testing_time": testing_time,
                },
            }

            print(input_data)

            # 调用AI分析函数
            result = ai_analysis(input_data, mode="slow")

            # 根据返回结果显示信息
            if result["status"] == "success":
                st.success("分析完成！以下为详细结果：")
                all_results = result.get("result", {})
                analysis_results = all_results.get("指标逐一分析", {})

                # 分块显示单一指标分析
                st.markdown("#### 指标逐一分析")
                # 定义卡片样式
                full_card_style = """
                <div style="background-color: {background_color}; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                    <h5 style="color: #333; margin-bottom: 10px;">{title}{abnormal_tag}</h5>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #555; margin-bottom: 10px;">
                        <span><strong>当前值：</strong>{current_value}</span>
                        <span><strong>指标区间：</strong>{range}</span>
                        <span><strong>指标结果：</strong>{result}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #555;">
                        <span><strong>指标解读：</strong>{interpretation}</span>
                        <span><strong>用药建议：</strong>{recommendation}</span>
                        <span><strong>参考文件(仅作示意)：</strong>{reference}</span>
                    </div>
                </div>
                """
                without_recommendation_card_style = """
                <div style="background-color: {background_color}; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);">
                    <h5 style="color: #333; margin-bottom: 10px; ">{title}{abnormal_tag}</h5>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #555; margin-bottom: 10px;">
                        <span><strong>当前值：</strong>{current_value}</span>
                        <span><strong>指标区间：</strong>{range}</span>
                        <span><strong>指标结果：</strong>{result}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #555;">
                        <span><strong>指标解读：</strong>{interpretation}</span>
                        <span><strong>参考文件(仅作示意)：</strong>{reference}</span>
                    </div>
                </div>
                """

                for indicator, analysis in analysis_results.items():
                    # 判断是否异常并设置背景颜色
                    background_color = "#f9f9f9"  # 默认背景色
                    abnormal_tag = ""  # 默认没有异常提示
                    if analysis["是否异常"]:
                        background_color = "#ffe6e6"  # 浅红色背景
                        abnormal_tag = """<span style="background-color: #ff0000; color: #fff; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-left: 20px;">
                                          异常
                                          </span>"""

                    # 如果 interpretation 为空，则不渲染该字段
                    if analysis["用药建议"]:
                        st.markdown(
                            full_card_style.format(
                                background_color=background_color,
                                title=analysis["标题"],
                                abnormal_tag=abnormal_tag,
                                current_value=analysis["当前值"],
                                range=analysis["参考区间"],
                                result=analysis["指标结果"],
                                interpretation=analysis["指标解读"],
                                recommendation=analysis["用药建议"],
                                reference=analysis["参考文件"],
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            without_recommendation_card_style.format(
                                background_color=background_color,
                                title=analysis["标题"],
                                abnormal_tag=abnormal_tag,
                                current_value=analysis["当前值"],
                                range=analysis["参考区间"],
                                result=analysis["指标结果"],
                                interpretation=analysis["指标解读"],
                                reference=analysis["参考文件"],
                            ),
                            unsafe_allow_html=True,
                        )

                # 综合分析及建议
                st.markdown("#### 综合分析及建议")
                # st.markdown(f"- **结论解读：** {analysis_results['summary']['conclusion']}")
                # st.markdown(f"- **用药建议：** {analysis_results['summary']['medication']}")
                # st.markdown(f"- **生活方式建议：** {analysis_results['summary']['lifestyle']}")
                # st.markdown(f"- **复测建议：** {analysis_results['summary']['retest']}")
                # st.markdown(f"- **风险提示：** {analysis_results['summary']['risk_warning']}")
                # 定义综合分析卡片样式
                summary_card_style = """
                <div style="background-color: #f0f8ff; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">
                    <div style="display: flex; flex-direction: column; gap: 5px; font-size: 13px; color: #555;">
                        <span><strong>结论解读：</strong>{overall_interpretation}</span>
                        <span><strong>用药建议：</strong>{medication_recommendation}</span>
                        <span><strong>生活方式建议：</strong>{lifestyle_recommendation}</span>
                        <span><strong>复诊建议：</strong>{follow_up_suggestion}</span>
                        <span><strong>参考依据：</strong>{reference}</span>
                    </div>
                </div>
                """

                overall_results = all_results.get("综合分析及建议", "")
                overall_interpretation = overall_results.get("结论解读", "")
                medication_recommendation = overall_results.get("用药建议", "")
                lifestyle_recommendation = overall_results.get("生活方式建议", "")
                reference = overall_results.get("参考依据", "")
                follow_up_suggestion = overall_results.get("复诊建议", "")

                # 渲染综合分析卡片
                st.markdown(
                    summary_card_style.format(
                        overall_interpretation=overall_interpretation,
                        medication_recommendation=medication_recommendation,
                        lifestyle_recommendation=lifestyle_recommendation,
                        follow_up_suggestion=follow_up_suggestion,
                        reference=reference,
                    ),
                    unsafe_allow_html=True,
                )

                # 可视化展示
                st.markdown("#### 数据图表")
                st.text("正在进行中... 很快就来")
                # st.markdown("以下为患者各项指标的变化趋势和对比分析：")
                #
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.markdown("#### 当前指标变化趋势")
                #     # 绘制趋势折线图（示例）
                #     st.line_chart(analysis_results['trend_data'])
                # with col2:
                #     st.markdown("#### 全国数据对比")
                #     # 显示柱状图或分布图（示例）
                #     st.bar_chart(analysis_results['comparison_data'])

                # st.markdown("#### 骨密度变化对比")
                # 骨密度变化图（示例）
                # st.line_chart(analysis_results['bone_density_trend'])
            else:
                st.error(result["message"])