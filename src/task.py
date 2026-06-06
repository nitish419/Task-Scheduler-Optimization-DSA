# src/task.py

class Task:
    def __init__(self, task_id, name, deadline, profit):
        self.task_id = task_id
        self.name = name
        self.deadline = deadline
        self.profit = profit

    def __repr__(self):
        return f"[{self.task_id}] {self.name} (Deadline: {self.deadline}, Profit: {self.profit})"