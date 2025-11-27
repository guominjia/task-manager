# Task Manager — 四象限任务看板 (Urgent/Important Matrix)

这是一个基于 Streamlit 的小型任务管理示例，采用史蒂芬·柯维的“时间管理四象限”（The Urgent/Important Matrix）来帮助对任务进行优先级划分。

This is a lightweight Streamlit task manager demo implementing Stephen Covey's Urgent/Important Matrix to help prioritize tasks.

## 🚀 主要功能 / Features

- 四象限看板：把任务按“紧急/重要”分为 I/II/III/IV 四象限进行展示。
- 添加/清除任务：通过表单添加任务，使用 session state 在单次应用运行中保留任务。
- 时间上下文：侧边栏显示当前日期、周数和月份。

Features:

- 4-quadrant board (Urgent/Important)
- Add and clear tasks via form
- Time context (date, ISO week, month) in the sidebar

## 快速开始 / Quick start (Windows PowerShell)

1. 建议创建并激活一个虚拟环境（可选但推荐）：

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. 安装依赖：

```powershell
pip install -r requirements.txt
```

3. 运行应用：

```powershell
streamlit run main.py
```

打开浏览器中 Streamlit 给出的本地地址查看界面（通常是 http://localhost:8501）。

## 使用说明 / Usage

- 在页面上填写任务标题、描述、选择紧迫/重要维度并提交。
- 应用将在界面上把任务放到对应的象限里。当前实现使用 `st.session_state` 保存任务，仅在应用运行期间持久。

Notes:

- For longer-term persistence consider connecting a database (SQLite, Postgres) or saving to a file (JSON/CSV).

## 设计与实现要点 / Implementation notes

- 看板布局使用 `st.columns(2)` 将页面左右分区，并在每一侧用不同容器形成四个象限。
- 使用 `st.form` 和 `st.radio` 控件确保用户输入被明确提交。
- 时间信息由 Python 的 `datetime` 模块计算并显示在侧边栏。

## 贡献 / Contributing

欢迎 fork、issue 和 pull request。建议先在 issue 中描述你想添加的功能或修复的 bug。

## 许可证 / License

本项目遵循仓库根目录中的 `LICENSE` 文件。

## 参考 / References

- Stephen R. Covey  The 7 Habits of Highly Effective People (Urgent/Important Matrix)
- (原始灵感来源链接) https://gemini.google.com/app/48bec8bcc1b64a45
