# daily_dashboard.py - Task Dashboard with Notes & Filters ✨

import streamlit as st
import datetime
import os

TASKS_FILE = "my_tasks.txt"
COMPLETED_TASKS_FILE = "completed_tasks.txt"

# Load existing tasks
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = [line.strip().split(" | ") for line in file.readlines()]
        return tasks  # [task, category, due_date, recurrence, notes]
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        file.writelines([f"{task} | {category} | {due_date} | {recurrence} | {notes}\n" for task, category, due_date, recurrence, notes in tasks])

# Add a new task
def add_task(task, category, due_date, recurrence, notes):
    tasks = load_tasks()
    tasks.append((task, category, due_date, recurrence, notes))
    save_tasks(tasks)

# Mark a task as completed
def mark_task_completed(task_index):
    tasks = load_tasks()
    completed_task = tasks.pop(task_index)
    save_tasks(tasks)
    with open(COMPLETED_TASKS_FILE, "a") as file:
        file.write(" | ".join(completed_task) + "\n")

# Filter tasks
def filter_tasks(tasks, show_overdue, show_only_recurring):
    today = datetime.date.today()
    filtered_tasks = []

    for task, category, due_date, recurrence, notes in tasks:
        due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        is_overdue = due_date_obj < today
        is_recurring = recurrence in {"daily", "weekly", "monthly"}

        if show_overdue and is_overdue:
            filtered_tasks.append((task, category, due_date, recurrence, notes))
        elif show_only_recurring and is_recurring:
            filtered_tasks.append((task, category, due_date, recurrence, notes))
        elif not show_overdue and not show_only_recurring:
            filtered_tasks.append((task, category, due_date, recurrence, notes))

    return filtered_tasks

# Main Interface
st.set_page_config(page_title="Task Dashboard", page_icon="✅", layout="wide")
st.title("✨ Your Snazzy Task Dashboard ✨")
st.sidebar.header("Manage Your Tasks")

# Task Filters
tasks = load_tasks()
st.sidebar.subheader("Filter Tasks")
show_overdue = st.sidebar.checkbox("Show Overdue Tasks Only")
show_only_recurring = st.sidebar.checkbox("Show Recurring Tasks Only")

filtered_tasks = filter_tasks(tasks, show_overdue, show_only_recurring)

# Display Tasks
st.header("📋 Task List")
if filtered_tasks:
    for i, (task, category, due_date, recurrence, notes) in enumerate(filtered_tasks):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        col1.write(f"**{task}**")
        col2.write(f"Category: `{category}`")
        col3.write(f"Due: `{due_date}`")
        col4.write(f"Recurring: `{recurrence.capitalize()}`" if recurrence != "none" else "One-Time Task")
        st.write(f"📝 **Notes**: _{notes or 'No notes provided.'}_")
        if st.button("Mark Complete", key=f"complete_{i}"):
            mark_task_completed(i)
            st.experimental_rerun()
else:
    st.info("No tasks to display. Time to add some!")

# Add Task Form
st.sidebar.subheader("Add New Task")
new_task = st.sidebar.text_input("Task Name")
new_category = st.sidebar.selectbox("Category", ["Chrysty", "Counsel", "EO", "Other"])
new_due_date = st.sidebar.date_input("Due Date", datetime.date.today())
new_recurrence = st.sidebar.selectbox("Recurrence", ["none", "daily", "weekly", "monthly"])
new_notes = st.sidebar.text_area("Notes (Optional)")
if st.sidebar.button("Add Task"):
    add_task(new_task, new_category, new_due_date.strftime("%Y-%m-%d"), new_recurrence, new_notes)
    st.sidebar.success("Task added!")
    st.experimental_rerun()