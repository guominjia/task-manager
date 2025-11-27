史蒂芬·柯维的\*\*“时间管理四象限”（The Urgent/Important Matrix）\*\*是一个高效能人士管理任务的经典框架。



\## 🚀 运行方法

1. 安装依赖：

```bash

pip install -r requirements.txt

```



2\. 运行应用：

```bash

streamlit run main.py

```

3\. ✨ 应用特性实现说明

* 四象限看板：使用 st.columns(2) 将屏幕分为左右两列，左侧放紧迫任务（I, III），右侧放不紧迫任务（II, IV），形成四块区域。
* 任务添加：使用 st.form 确保输入数据只有在点击提交按钮后才会被处理和清空。
* 紧迫性与重要性维度：使用 st.radio 控件来确定任务的象限，用户只能选择“重要/不重要”和“紧迫/不紧迫”。
* 日历、周、月信息：利用 Python 内置的 datetime 库，在侧边栏 (st.sidebar) 显示当前日期、本年度的周数 (isocalendar()) 和当前月份，为用户提供时间上下文。
* 数据持久性：代码中使用了 st.session\_state 来存储任务列表。这意味着只要 Streamlit 应用保持运行，任务就不会丢失。如果需要更长期的存储，则需要集成如 SQLite 或云端数据库。



\## 参考

https://gemini.google.com/app/48bec8bcc1b64a45

