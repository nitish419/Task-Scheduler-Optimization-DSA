import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.task import Task
from src.scheduler import optimize_schedule

# Set the modern theme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TaskSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Task Scheduler Optimization System")
        self.geometry("900x600")
        self.resizable(False, False)

        # Internal state
        self.tasks = []
        self.task_counter = 1

        self.setup_ui()

    def setup_ui(self):
        # --- LEFT FRAME: INPUTS ---
        self.left_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.left_frame, text="Add New Task", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # Task Name Input
        self.name_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Task Name (e.g. UI Fix)", width=250)
        self.name_entry.pack(pady=10)

        # Deadline Input
        self.deadline_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Deadline (integer)", width=250)
        self.deadline_entry.pack(pady=10)

        # Profit/Priority Input
        self.profit_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Profit / Score (integer)", width=250)
        self.profit_entry.pack(pady=10)

        # Add Button
        self.add_btn = ctk.CTkButton(self.left_frame, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=20)

        # Run Optimization Button
        self.run_btn = ctk.CTkButton(self.left_frame, text="▶ Run Optimization", fg_color="#28a745", hover_color="#218838", command=self.run_optimization)
        self.run_btn.pack(pady=(50, 10))
        
        # Clear Button
        self.clear_btn = ctk.CTkButton(self.left_frame, text="Clear All", fg_color="#dc3545", hover_color="#c82333", command=self.clear_all)
        self.clear_btn.pack(pady=10)

        # --- RIGHT FRAME: OUTPUTS ---
        self.right_frame = ctk.CTkFrame(self, width=550, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        # Pending Tasks List
        self.pending_label = ctk.CTkLabel(self.right_frame, text="Pending Tasks", font=ctk.CTkFont(size=16, weight="bold"))
        self.pending_label.pack(pady=(10, 5))

        self.pending_textbox = ctk.CTkTextbox(self.right_frame, height=150, width=500)
        self.pending_textbox.pack(pady=5)
        self.pending_textbox.configure(state="disabled")

        # Optimization Results
        self.results_label = ctk.CTkLabel(self.right_frame, text="Optimization Results", font=ctk.CTkFont(size=16, weight="bold"))
        self.results_label.pack(pady=(20, 5))

        self.results_textbox = ctk.CTkTextbox(self.right_frame, height=250, width=500)
        self.results_textbox.pack(pady=5)
        self.results_textbox.configure(state="disabled")

    def add_task(self):
        name = self.name_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        profit = self.profit_entry.get().strip()

        # Validation
        if not name or not deadline or not profit:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            deadline = int(deadline)
            profit = int(profit)
        except ValueError:
            messagebox.showerror("Input Error", "Deadline and Profit must be integers.")
            return

        # Create Task object
        task_id = f"T{self.task_counter}"
        new_task = Task(task_id, name, deadline, profit)
        self.tasks.append(new_task)
        self.task_counter += 1

        # Update UI
        self.append_to_textbox(self.pending_textbox, f"[{task_id}] {name} | Deadline: {deadline} | Profit: {profit}\n")
        
        # Clear inputs
        self.name_entry.delete(0, 'end')
        self.deadline_entry.delete(0, 'end')
        self.profit_entry.delete(0, 'end')

    def run_optimization(self):
        if not self.tasks:
            messagebox.showwarning("No Tasks", "Please add tasks before optimizing.")
            return

        # We must pass a copy of the list because the algorithm sorts it in place
        time_slots, scheduled, missed, total_profit = optimize_schedule(self.tasks.copy())

        # Clear previous results
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")

        output_text = "--- OPTIMIZED EXECUTION ORDER ---\n"
        for i in range(1, len(time_slots)):
            if time_slots[i] != -1:
                task_name = next(t.name for t in scheduled if t.task_id == time_slots[i])
                output_text += f"Slot {i}: {task_name} (ID: {time_slots[i]})\n"
            else:
                output_text += f"Slot {i}: [ IDLE ]\n"

        output_text += f"\n💰 Total Profit/Score: {total_profit}\n"

        output_text += "\n--- MISSED TASKS ---\n"
        if not missed:
            output_text += "None! All tasks scheduled.\n"
        else:
            for m in missed:
                output_text += f"❌ {m.name} (Deadline: {m.deadline})\n"

        self.append_to_textbox(self.results_textbox, output_text)

    def clear_all(self):
        self.tasks.clear()
        self.task_counter = 1
        
        self.pending_textbox.configure(state="normal")
        self.pending_textbox.delete("1.0", "end")
        self.pending_textbox.configure(state="disabled")

        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.configure(state="disabled")

    def append_to_textbox(self, textbox, text):
        textbox.configure(state="normal")
        textbox.insert("end", text)
        textbox.configure(state="disabled")

if __name__ == "__main__":
    app = TaskSchedulerApp()
    app.mainloop()