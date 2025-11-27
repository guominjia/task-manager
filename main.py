import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.colored_header import colored_header # 这是一个流行的社区组件，用于美化标题
# 备注：你需要安装 streamlit-extras: pip install streamlit-extras

# --- 1. 数据结构：任务存储 ---
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
    # 示例初始任务
    st.session_state['tasks'].extend([
        {'id': 1, 'name': '准备下周会议报告', 'due_date': '2025-12-02', 'urgency': '重要', 'importance': '紧迫'}, # I 象限
        {'id': 2, 'name': '学习新的编程语言', 'due_date': '2025-12-31', 'urgency': '重要', 'importance': '不紧迫'}, # II 象限
        {'id': 3, 'name': '处理突发邮件', 'due_date': '2025-11-26', 'urgency': '不重要', 'importance': '紧迫'}, # III 象限
        {'id': 4, 'name': '整理旧文件', 'due_date': '2026-01-01', 'urgency': '不重要', 'importance': '不紧迫'}, # IV 象限
    ])
    st.session_state['next_id'] = len(st.session_state['tasks']) + 1

# --- 辅助函数：添加任务 ---
def add_task(name, due_date, urgency, importance):
    new_task = {
        'id': st.session_state['next_id'],
        'name': name,
        'due_date': due_date.strftime('%Y-%m-%d'),
        'urgency': urgency,
        'importance': importance,
    }
    st.session_state['tasks'].append(new_task)
    st.session_state['next_id'] += 1
    st.toast(f'任务 "{name}" 添加成功！', icon='✅')

# --- 辅助函数：根据象限过滤任务 ---
def filter_tasks(tasks_list, urgency_val, importance_val):
    return [
        task['name']
        for task in tasks_list
        if task['urgency'] == urgency_val and task['importance'] == importance_val
    ]

# --- 2. 页面布局 ---
st.set_page_config(layout="wide", page_title="柯维四象限任务管理")
st.title("🗓️ 高效能任务管理（四象限法）")

# --- 3. 日历/周月信息侧边栏 ---
with st.sidebar:
    st.header("🕰️ 时间信息")
    today = datetime.now()
    st.metric(label="今天是", value=today.strftime("%Y年%m月%d日"))
    
    # 星期信息
    week_number = today.isocalendar()[1]
    st.info(f"本周是本年的第 **{week_number}** 周。")
    
    # 月份信息
    st.warning(f"当前月份是 **{today.month}** 月。")

    st.subheader("➕ 添加新任务")
    with st.form("task_form", clear_on_submit=True):
        new_name = st.text_input("任务名称", max_chars=100)
        new_due_date = st.date_input("截止日期", min_value=today.date())
        
        # 确定象限的维度选择
        new_importance = st.radio(
            "重要性（Importance）",
            ['重要', '不重要'],
            horizontal=True
        )
        new_urgency = st.radio(
            "紧迫性（Urgency）",
            ['紧迫', '不紧迫'],
            horizontal=True
        )
        
        submitted = st.form_submit_button("保存任务")
        if submitted and new_name:
            add_task(new_name, new_due_date, new_urgency, new_importance)
            # 重新运行以更新看板
            st.rerun()

# --- 4. 四象限看板展示 ---

# 将任务列表转换为 DataFrame 便于处理
df_tasks = pd.DataFrame(st.session_state['tasks'])

# 象限布局
col1, col2 = st.columns(2)

# --- 紧迫性（Urgent）象限 ---

# I. 重要且紧迫 (Quadrant I: Important & Urgent)
with col1:
    colored_header(
        label="🔴 I. 重要且紧迫（Crisis）",
        description="危机、问题、紧迫项目。**立即去做**。",
        color_name="red-70",
    )
    tasks_I = filter_tasks(st.session_state['tasks'], '重要', '紧迫')
    for task in tasks_I:
        st.markdown(f"* **{task}**")

# III. 不重要但紧迫 (Quadrant III: Not Important & Urgent)
with col1:
    colored_header(
        label="🟡 III. 不重要但紧迫（Distraction）",
        description="某些电话、邮件、别人的小事。**授权或拒绝**。",
        color_name="yellow-70",
    )
    tasks_III = filter_tasks(st.session_state['tasks'], '不重要', '紧迫')
    for task in tasks_III:
        st.markdown(f"* {task}")

# --- 不紧迫性（Not Urgent）象限 ---

# II. 重要但不紧迫 (Quadrant II: Important & Not Urgent)
with col2:
    colored_header(
        label="🟢 II. 重要但不紧迫（Focus）",
        description="预防措施、关系建立、规划、新机会。**规划去做（高效核心）**。",
        color_name="green-70",
    )
    tasks_II = filter_tasks(st.session_state['tasks'], '重要', '不紧迫')
    for task in tasks_II:
        st.markdown(f"* **{task}**")

# IV. 不重要且不紧迫 (Quadrant IV: Not Important & Not Urgent)
with col2:
    colored_header(
        label="🔵 IV. 不重要且不紧迫（Waste）",
        description="琐事、一些时间浪费。**消除**。",
        color_name="blue-70",
    )
    tasks_IV = filter_tasks(st.session_state['tasks'], '不重要', '不紧迫')
    for task in tasks_IV:
        st.markdown(f"* {task}")

# --- 5. 详细任务列表（可选） ---
st.markdown("---")
st.subheader("📚 所有任务详情")
st.dataframe(df_tasks, use_container_width=True)

# 提示：实际应用中，你可能需要添加**删除**和**标记完成**的功能。