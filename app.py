# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 模拟数据库
supplier_db = {
    "suppliers": [
        {"id": "RF-202403", "name": "锐锋精密", "category": "电池托盘", 
         "qualification": "A级", "price": 15800, "delivery_score": 92}
    ],
    "conflicts": [
        {"event_id": "C-001", "supplier_id": "RF-202403", 
         "conflict_type": "三重冲突", "status": "已解决"}
    ],
    "arbitrations": [
        {"event_id": "C-001", "resolution": "有条件通过", 
         "conditions": ["试用期3个月", "首付30%", "补充尽调"]}
    ]
}

# 页面配置
st.set_page_config(page_title="链智审系统演示", layout="wide")

# 标题区
st.title("🛠️ 供应链AI协同审核系统 - 链智审")
st.markdown("---")

# 功能模块
with st.sidebar:
    st.header("导航")
    page = st.radio("选择演示模块", ["冲突场景模拟", "仲裁工作流", "实施案例库"])
    
    # 参数调节
    st.header("参数调节")
    base_price = st.slider("设定基准价格（万元）", 10.0, 20.0, 14.2)
    risk_threshold = st.slider("风险阈值（0-100）", 0, 100, 60)

# 场景模拟页
if page == "冲突场景模拟":
    st.header("🔍 供应商资质审核冲突模拟")
    
    current_price = supplier_db["suppliers"][0]["price"] / 10000
    price_deviation = (current_price - base_price) / base_price * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("采购部门")
        st.metric("交付能力评分", "92/100", delta="推荐等级A")
        st.progress(0.92)
        with st.expander("查看审核逻辑"):
            st.code("""历史交付准时率：98%
资质证书：ISO9001, IATF16949
合作稳定性：5年无中断""")
        
    with col2:
        st.subheader("法务部门")
        risk_level = "高" if risk_threshold < 70 else "中"
        st.metric("风险评级", risk_level, delta="1条关联诉讼", delta_color="inverse")
        with st.expander("查看风险详情"):
            st.code("""关联企业：迅达物流
案由：运输合同纠纷（2023沪01民终1234号）
影响评估：供应链中断风险+15%""")
        
    with col3:
        st.subheader("财务部门")
        st.metric("价格偏离度", f"{price_deviation:.1f}%", 
                 delta="超出阈值" if abs(price_deviation)>5 else "在允许范围内", 
                 delta_color="inverse" if abs(price_deviation)>5 else "normal")
        with st.expander("成本分析"):
            st.code(f"""市场基准价：¥{base_price:.1f}万
当前报价：¥{current_price:.1f}万
允许浮动：±5%""")
    
    st.markdown("---")
    st.subheader("动态冲突分析")
    
    df = pd.DataFrame({
        "指标": ["交付能力", "合规风险", "成本控制"],
        "当前值": [92, 35, 68],
        "阈值": [80, risk_threshold, 70]
    })
    
    fig = px.bar(df, x="指标", y=["当前值", "阈值"], 
                barmode="group", text_auto=True,
                title="部门指标对比分析")
    st.plotly_chart(fig, use_container_width=True)

# 工作流页
elif page == "仲裁工作流":
    st.header("⚙️ 三阶治理工作流演示")
    
    tab1, tab2, tab3, tab4 = st.tabs(["冲突识别", "仲裁会议", "系统连携", "执行跟踪"])
    
    with tab1:
        st.subheader("阶段1：冲突分类矩阵")
        matrix_df = pd.DataFrame([
            ["单一指标超标", "自动补偿谈判", "2小时"],
            ["双重目标冲突", "部门联席预审", "8小时"],
            ["三重冲突+置信差异", "AI仲裁委员会", "24小时"]
        ], columns=["冲突类型", "处理通道", "时限"])
        
        st.dataframe(matrix_df.style.highlight_max(axis=0), 
                    use_container_width=True)
        
        st.write("**当前冲突检测**:")
        st.json({
            "冲突类型": "三重冲突+置信差异",
            "触发流程": "提交AI仲裁委员会",
            "处理时限": "24小时"
        })
        
    with tab2:
        st.subheader("仲裁会议进程")
        
        # 时间线数据
        timeline_df = pd.DataFrame([
            {"阶段": "会前准备", "状态": "已完成", "耗时": 2, "负责人": "系统自动"},
            {"阶段": "证据调取", "状态": "进行中", "耗时": 1, "负责人": "内审部"},
            {"阶段": "多方听证", "状态": "待处理", "耗时": 3, "负责人": "仲裁主席"},
            {"阶段": "决议生成", "状态": "待处理", "耗时": 1, "负责人": "AI顾问"}
        ])
        
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("**会议进程甘特图**")
            fig = px.timeline(timeline_df, 
                            x_start=[0,2,3,6],  # 开始时间
                            x_end=[2,3,6,7],    # 结束时间
                            y="阶段", 
                            color="状态",
                            title="仲裁进度跟踪",
                            color_discrete_map={
                                "已完成": "#4CAF50",
                                "进行中": "#FFC107",
                                "待处理": "#E0E0E0"
                            })
            fig.update_xaxes(title_text="处理时长（小时）")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**联系人矩阵**")
            contact_matrix = pd.DataFrame([
                ["采购代表", "王悦", "采购专员", "wangyue@demo.com"],
                ["法务代表", "张涛", "法务经理", "zhangtao@demo.com"],
                ["财务代表", "陈敏", "财务总监", "chenmin@demo.com"],
                ["仲裁主席", "李航", "供应链总监", "lihang@demo.com"]
            ], columns=["角色", "姓名", "职位", "联系方式"])
            st.dataframe(contact_matrix, hide_index=True)
            
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**外部环境指标**")
            st.metric("行业风险指数", "58.2", delta="+2.1 vs上月", 
                      help="来源：行业监管数据平台")
            st.metric("原材料价格趋势", "↑3.2%", delta_color="inverse",
                     help="本月大宗商品价格波动")
            
        with c2:
            st.markdown("**企业风控参数**")
            st.metric("最大风险容忍度", "75/100", 
                     help="董事会设定年度阈值")
            st.metric("紧急采购溢价上限", "15%", 
                     help="特殊情况下允许的溢价空间")
            
        with c3:
            st.markdown("**实时投票机制**")
            vote_status = st.radio("模拟表决选项", 
                                  ["赞成", "有条件通过", "否决"], 
                                  horizontal=True)
            st.progress(66, f"当前共识度：66%")
            st.caption("需达成>60%共识方可生效")
    
    with tab3:
        st.subheader("系统连携拓扑")
        
        # 拓扑图数据
        nodes = pd.DataFrame([
            {"节点": "链智审核心", "类型": "中枢系统", "x": 2, "y": 2},
            {"节点": "ERP", "类型": "业务系统", "x": 1, "y": 1},
            {"节点": "合同数据库", "类型": "法务系统", "x": 3, "y": 1},
            {"节点": "财务中台", "类型": "财务系统", "x": 2, "y": 0},
            {"节点": "舆情监控", "类型": "外部数据", "x": 4, "y": 2}
        ])
        
        edges = [
            {"来源": "链智审核心", "目标": "ERP", "类型": "实时数据"},
            {"来源": "链智审核心", "目标": "合同数据库", "类型": "API调用"},
            {"来源": "链智审核心", "目标": "财务中台", "类型": "双向同步"},
            {"来源": "链智审核心", "目标": "舆情监控", "类型": "数据抓取"}
        ]
        
        fig = px.scatter(nodes, x="x", y="y",
                        size=[30,20,20,20,20],
                        color="类型",
                        text="节点",
                        title="系统集成拓扑图")
        
        # 添加连接线
        for edge in edges:
            source = nodes[nodes["节点"] == edge["来源"]].iloc[0]
            target = nodes[nodes["节点"] == edge["目标"]].iloc[0]
            fig.add_shape(
                type="line",
                x0=source["x"], y0=source["y"],
                x1=target["x"], y1=target["y"],
                line=dict(color="#BDBDBD", width=2)
            )
            
        fig.update_traces(marker=dict(size=100),
                         textfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)
        
        # 数据流监控
        st.markdown("**实时数据流状态**")
        flow_df = pd.DataFrame([
            ["ERP→核心", "采购订单", "正常", "5ms"],
            ["法务→核心", "合同条款", "延迟", "320ms"],
            ["财务→核心", "成本数据", "正常", "8ms"],
            ["舆情→核心", "行业风险", "正常", "120ms"]
        ], columns=["通道", "数据类型", "状态", "延迟"])
        st.dataframe(flow_df.style.applymap(
            lambda x: "color: red" if x=="延迟" else None), 
            use_container_width=True)
    
    with tab4:
        st.subheader("执行追踪矩阵")
        task_df = pd.DataFrame([
            ["合同修订", "法务部", "内审部", "风险<30"],
            ["付款调整", "财务部", "供应链部", "偏差<5%"],
            ["关系维护", "采购部", "客户成功部", "评分≥4"]
        ], columns=["任务", "执行方", "监督方", "验收标准"])
        
        st.dataframe(task_df.style.applymap(
            lambda x: "background-color: #e6f3ff" if x=="法务部" else ""), 
            use_container_width=True)
        
        st.button("模拟完成通知", help="点击发送完成通知邮件")

# 案例库页
else:
    st.header("📚 实施案例库")
    
    case_filter = st.selectbox("筛选案例类型", [
        "全部", "三重冲突", "双重冲突", "单一冲突"
    ])
    
    case_df = pd.DataFrame({
        "案例ID": ["C-2023-045", "C-2024-012", "C-2024-018"],
        "冲突类型": ["三重冲突", "双重冲突", "单一冲突"],
        "处置方式": ["有条件通过", "调整后通过", "自动处理"],
        "处理时长": [24, 8, 2],
        "保留结果": ["成功合作", "进行中", "已终止"]
    })
    
    if case_filter != "全部":
        case_df = case_df[case_df["冲突类型"] == case_filter]
    
    st.dataframe(case_df, use_container_width=True)
    
    with st.expander("案例趋势分析"):
        fig = px.line(case_df, x="案例ID", y="处理时长",
                     title="案例处理效率趋势")
        st.plotly_chart(fig)

st.markdown("---")
st.caption("演示系统说明：本系统使用模拟数据展示核心业务流程")
