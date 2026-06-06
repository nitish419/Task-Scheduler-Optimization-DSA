# src/scheduler.py
import os

def optimize_schedule(tasks):
    tasks.sort(key=lambda x: x.profit, reverse=True)
    max_deadline = max(task.deadline for task in tasks) if tasks else 0
    time_slots = [-1] * (max_deadline + 1)
    
    scheduled_tasks = []
    missed_tasks = []
    total_profit = 0

    for task in tasks:
        placed = False
        for j in range(min(max_deadline, task.deadline), 0, -1):
            if time_slots[j] == -1: 
                time_slots[j] = task.task_id
                scheduled_tasks.append(task)
                total_profit += task.profit
                placed = True
                break
        
        if not placed:
            missed_tasks.append(task)

    return time_slots, scheduled_tasks, missed_tasks, total_profit

def generate_report(time_slots, scheduled_tasks, missed_tasks, total_profit):
    os.makedirs("outputs", exist_ok=True)
    report_path = "outputs/schedule_report.txt"
    
    with open(report_path, "w") as file:
        file.write("=== TASK SCHEDULER OPTIMIZATION REPORT ===\n\n")
        # ... (rest of the report generation code from before)
        
    print(f"\n[+] Success! Report generated at: {report_path}")