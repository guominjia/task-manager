import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.colored_header import colored_header # 这是一个流行的社区组件，用于美化标题

# --- 1. 数据结构：任务存储（新增 'completed' 字段） ---
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
    # 示例初始任务，新增 'completed' 字段
    st.session_state['tasks'].extend([
        {'id': 1, 'name': '准备下周会议报告', 'due_date': '2025-12-02', 'importance': '重要', 'urgency': '紧迫', 'completed': False}, # I 象限
        {'id': 2, 'name': '学习新的编程语言', 'due_date': '2025-12-31', 'importance': '重要', 'urgency': '不紧迫', 'completed': False}, # II 象限
        {'id': 3, 'name': '处理突发邮件', 'due_date': '2025-11-26', 'importance': '不重要', 'urgency': '紧迫', 'completed': True}, # III 象限
        {'id': 4, 'name': '整理旧文件', 'due_date': '2026-01-01', 'importance': '不重要', 'urgency': '不紧迫', 'completed': False}, # IV 象限
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
        'completed': False, # 新任务默认为未完成
    }
    st.session_state['tasks'].append(new_task)
    st.session_state['next_id'] += 1
    st.toast(f'任务 "{name}" 添加成功！', icon='✅')

# --- 辅助函数：删除任务 ---
def delete_task(task_id):
    st.session_state['tasks'] = [task for task in st.session_state['tasks'] if task['id'] != task_id]
    st.toast('任务已删除！', icon='🗑️')

# --- 辅助函数：标记完成/取消完成 ---
def toggle_complete(task_id):
    for task in st.session_state['tasks']:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            action = "完成" if task['completed'] else "取消完成"
            st.toast(f'任务 "{task["name"]}" 已标记为 **{action}**！', icon='👍')
            break

# --- 辅助函数：根据象限和状态过滤并渲染任务（新增颜色编码） ---
def render_quadrant(urgency_val, importance_val, title, description, header_color, emoji):
    # 使用社区组件 colored_header（如果没有安装，可以注释掉并使用 st.subheader）
    # colored_header(label=title, description=description, color_name=header_color)
    st.subheader(f"{emoji} {title}")
    st.markdown(f"*{description}*")
    
    # 过滤出当前象限的未完成任务
    tasks_to_render = [
        task
        for task in st.session_state['tasks']
        if task['urgency'] == urgency_val and task['importance'] == importance_val and not task['completed']
    ]
    
    # 获取已完成任务（只用于展示，不带操作按钮）
    completed_tasks = [
        task
        for task in st.session_state['tasks']
        if task['urgency'] == urgency_val and task['importance'] == importance_val and task['completed']
    ]

    # **未完成任务渲染（带操作按钮）**
    if tasks_to_render:
        st.markdown("---")
        st.caption("**待处理任务**")
        for task in tasks_to_render:
            # 颜色编码 (I: 红色, II: 绿色, III: 黄色, IV: 蓝色)
            text_color = "red" if header_color == "red-70" else \
                         "green" if header_color == "green-70" else \
                         "orange" if header_color == "yellow-70" else \
                         "blue"
            
            # 使用 HTML 和 Markdown 混合实现颜色编码
            st.markdown(
                f'<span style="color:{text_color};">**{task["name"]}**</span> | 截止日期: {task["due_date"]}', 
                unsafe_allow_html=True
            )
            
            # 操作按钮放在一列中
            col_comp, col_del = st.columns([1, 1], gap="small")
            with col_comp:
                st.button("✅ 标记完成", key=f"comp_{task['id']}", on_click=toggle_complete, args=(task['id'],))
            with col_del:
                st.button("🗑️ 删除", key=f"del_{task['id']}", on_click=delete_task, args=(task['id'],))
            st.markdown("---")
    else:
        st.info("当前象限没有待处理任务。")
        
    # **已完成任务渲染（带操作按钮）**
    if completed_tasks:
        st.caption("**已完成任务**")
        with st.expander("点击查看已完成任务"):
            for task in completed_tasks:
                st.markdown(f'~~{task["name"]}~~ (于 {task["due_date"]} 截止)')
                
                # 操作按钮放在一列中
                col_uncomp, col_del = st.columns([1, 1], gap="small")
                with col_uncomp:
                    st.button("🔄 取消完成", key=f"uncomp_{task['id']}", on_click=toggle_complete, args=(task['id'],))
                with col_del:
                    st.button("🗑️ 删除", key=f"del_comp_{task['id']}", on_click=delete_task, args=(task['id'],))
            st.markdown("---")


# --- 2. 页面布局 ---
st.set_page_config(layout="wide", page_title="柯维四象限任务管理")
st.title("🗓️ 高效能任务管理（四象限法）")

# --- 3. 日历/周月信息侧边栏 + 新任务表单 ---
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
        
        new_importance = st.radio("重要性（Importance）", ['重要', '不重要'], horizontal=True)
        new_urgency = st.radio("紧迫性（Urgency）", ['紧迫', '不紧迫'], horizontal=True)
        
        submitted = st.form_submit_button("保存任务")
        if submitted and new_name:
            add_task(new_name, new_due_date, new_urgency, new_importance)
            # 重新运行以更新看板
            st.rerun()

# --- 4. 四象限看板展示 ---

# 象限布局
col1, col2 = st.columns(2)

# I. 重要且紧迫 (Quadrant I: Important & Urgent)
with col1:
    render_quadrant(
        importance_val='重要', urgency_val='紧迫', 
        title="I. 重要且紧迫（Crisis）", 
        description="危机、问题、紧迫项目。立即去做。", 
        header_color="red-70", 
        emoji="🔴"
    )

# II. 重要但不紧迫 (Quadrant II: Important & Not Urgent)
with col2:
    render_quadrant(
        importance_val='重要', urgency_val='不紧迫', 
        title="II. 重要但不紧迫（Focus）", 
        description="预防措施、关系建立、规划、新机会。规划去做（高效核心）。", 
        header_color="green-70", 
        emoji="🟢"
    )

# III. 不重要但紧迫 (Quadrant III: Not Important & Urgent)
with col1:
    render_quadrant(
        importance_val='不重要', urgency_val='紧迫', 
        title="III. 不重要但紧迫（Distraction）", 
        description="某些电话、邮件、别人的小事。授权或拒绝。", 
        header_color="yellow-70", 
        emoji="🟡"
    )

# IV. 不重要且不紧迫 (Quadrant IV: Not Important & Not Urgent)
with col2:
    render_quadrant(
        importance_val='不重要', urgency_val='不紧迫', 
        title="IV. 不重要且不紧迫（Waste）", 
        description="琐事、一些时间浪费。消除。", 
        header_color="blue-70", 
        emoji="🔵"
    )

# --- 5. 详细任务列表（可选，使用 dataframe 展示所有任务） ---
st.markdown("---")
st.subheader("📚 所有任务详情（数据表）")
df_tasks = pd.DataFrame(st.session_state['tasks'])
st.dataframe(df_tasks, use_container_width=True)