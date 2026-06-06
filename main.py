import os

# --- 1. DATA STRUCTURE: TASK CLASS ---
class Task:
    def __init__(self, task_id, name, deadline, profit):
        self.task_id = task_id
        self.name = name
        self.deadline = deadline
        self.profit = profit

    def __repr__(self):
        return f"[{self.task_id}] {self.name} (Deadline: {self.deadline}, Profit: {self.profit})"


# --- 2. CORE ALGORITHM: GREEDY SCHEDULER ---
def optimize_schedule(tasks):
    """
    Schedules tasks to maximize profit.
    Time Complexity: O(N log N) for sorting + O(N * max_deadline) for scheduling.
    Space Complexity: O(max_deadline) for time slots.
    """
    # Step 1: Sort tasks in descending order of their profit
    tasks.sort(key=lambda x: x.profit, reverse=True)

    # Step 2: Find the maximum deadline to create time slots
    max_deadline = max(task.deadline for task in tasks) if tasks else 0
    
    # Initialize time slots (0 to max_deadline). Slot 0 is unused for simplicity.
    time_slots = [-1] * (max_deadline + 1)
    
    scheduled_tasks = []
    missed_tasks = []
    total_profit = 0

    # Step 3: Iterate through sorted tasks and place them
    for task in tasks:
        placed = False
        # Try to place task as close to its deadline as possible
        for j in range(min(max_deadline, task.deadline), 0, -1):
            if time_slots[j] == -1: # If slot is empty
                time_slots[j] = task.task_id
                scheduled_tasks.append(task)
                total_profit += task.profit
                placed = True
                break
        
        if not placed:
            missed_tasks.append(task)

    return time_slots, scheduled_tasks, missed_tasks, total_profit


# --- 3. UTILITY: GENERATE REPORT ---
def generate_report(time_slots, scheduled_tasks, missed_tasks, total_profit):
    os.makedirs("outputs", exist_ok=True)
    report_path = "outputs/schedule_report.txt"
    
    with open(report_path, "w") as file:
        file.write("=== TASK SCHEDULER OPTIMIZATION REPORT ===\n\n")
        
        file.write("--- SCHEDULED TIMELINE ---\n")
        for i in range(1, len(time_slots)):
            if time_slots[i] != -1:
                # Find task name
                task_name = next(t.name for t in scheduled_tasks if t.task_id == time_slots[i])
                file.write(f"Time Slot {i}: {task_name} (ID: {time_slots[i]})\n")
            else:
                file.write(f"Time Slot {i}: [ IDLE ]\n")
                
        file.write(f"\nTotal Maximum Profit Achieved: {total_profit}\n")
        
        file.write("\n--- MISSED DEADLINES ---\n")
        if not missed_tasks:
            file.write("None! All possible tasks scheduled optimally.\n")
        else:
            for task in missed_tasks:
                file.write(f"- {task.name} (Deadline: {task.deadline}, Profit: {task.profit})\n")

    print(f"\n[+] Success! Report generated at: {report_path}")


# --- 4. CLI INTERFACE ---
def main():
    print("========================================")
    print("  TASK SCHEDULER OPTIMIZATION SYSTEM  ")
    print("========================================\n")

    # Sample Data Generation
    tasks = [
        Task("T1", "Database Backup", deadline=2, profit=100),
        Task("T2", "API Endpoint Fix", deadline=1, profit=19),
        Task("T3", "Server Maintenance", deadline=2, profit=27),
        Task("T4", "User UI Update", deadline=1, profit=25),
        Task("T5", "Security Patch", deadline=3, profit=15)
    ]

    print("--- INCOMING TASKS ---")
    for t in tasks:
        print(t)
    
    print("\n[!] Running Optimization Algorithm (Greedy Approach)...")
    time_slots, scheduled, missed, profit = optimize_schedule(tasks)

    print("\n--- OPTIMIZED EXECUTION ORDER ---")
    for i in range(1, len(time_slots)):
        if time_slots[i] != -1:
             print(f"Slot {i}: Task {time_slots[i]}")

    print(f"\nTotal Profit/Score: {profit}")
    
    print("\n--- MISSED TASKS ---")
    for m in missed:
        print(f"Task {m.task_id} missed deadline.")

    # Save to file
    generate_report(time_slots, scheduled, missed, profit)

if __name__ == "__main__":
    main()