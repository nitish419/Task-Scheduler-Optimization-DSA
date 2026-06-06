import streamlit as st
import pandas as pd
from src.task import Task
from src.scheduler import optimize_schedule

st.set_page_config(page_title="Task Scheduler Pro", layout="centered")

st.title("⏱️ Task Scheduler Optimization")
st.write("A Greedy Algorithm demonstration for optimal CPU/Task scheduling.")

# Initialize session state to store tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'task_counter' not in st.session_state:
    st.session_state.task_counter = 1

# --- INPUT SECTION ---
with st.form("task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Task Name")
    with col2:
        deadline = st.number_input("Deadline", min_value=1, step=1)
    with col3:
        profit = st.number_input("Profit/Score", min_value=1, step=1)
    
    submitted = st.form_submit_button("Add Task")
    
    if submitted and name:
        task_id = f"T{st.session_state.task_counter}"
        new_task = Task(task_id, name, int(deadline), int(profit))
        st.session_state.tasks.append(new_task)
        st.session_state.task_counter += 1
        st.success(f"Added {name}!")

# --- DISPLAY PENDING TASKS ---
if st.session_state.tasks:
    st.subheader("Pending Tasks")
    task_data = [{"ID": t.task_id, "Name": t.name, "Deadline": t.deadline, "Profit": t.profit} for t in st.session_state.tasks]
    st.dataframe(pd.DataFrame(task_data), use_container_width=True)

# --- OPTIMIZATION SECTION ---
colA, colB = st.columns([1, 4])
with colA:
    if st.button("Clear All", type="secondary"):
        st.session_state.tasks = []
        st.session_state.task_counter = 1
        st.rerun()

with colB:
    if st.button("▶ Run Optimizer", type="primary"):
        if not st.session_state.tasks:
            st.warning("Please add tasks first.")
        else:
            # Run your existing Python algorithm!
            time_slots, scheduled, missed, total_profit = optimize_schedule(st.session_state.tasks.copy())
            
            st.divider()
            st.subheader("📈 Optimization Results")
            st.metric("Total Maximum Profit", total_profit)
            
            st.write("**Execution Timeline:**")
            for i in range(1, len(time_slots)):
                if time_slots[i] != -1:
                    task_name = next(t.name for t in scheduled if t.task_id == time_slots[i])
                    st.success(f"**Slot {i}:** {task_name} (ID: {time_slots[i]})")
                else:
                    st.info(f"**Slot {i}:** [ IDLE ]")
            
            if missed:
                st.write("**Missed Deadlines:**")
                for m in missed:
                    st.error(f"❌ {m.name} (Deadline: {m.deadline})")