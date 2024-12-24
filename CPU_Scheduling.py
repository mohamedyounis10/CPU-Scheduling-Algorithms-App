import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Initialize CustomTkinter theme
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green")

class ProcessAttributes:
    def __init__(self, pid, BurstTime, ArrivalTime, Priority=0):
        self.pid = pid
        self.BurstTime = BurstTime
        self.ArrivalTime = ArrivalTime
        self.Priority = Priority
        self.RemainingTime = BurstTime  # For preemptive algorithms

# Scheduling Algorithms
def FCFS(process_list):
    time = 0
    process_list.sort(key=lambda x: x.ArrivalTime)
    process_times = []

    while process_list:
        if process_list[0].ArrivalTime > time:
            time += 1
        else:
            process = process_list.pop(0)
            start_time = time
            end_time = time + process.BurstTime
            process_times.append((process.pid, start_time, end_time))
            time = end_time

    return process_times

def SJF(process_list):
    time = 0
    process_list.sort(key=lambda x: x.ArrivalTime)
    process_times = []

    while process_list:
        available = [p for p in process_list if p.ArrivalTime <= time]
        if available:
            process = min(available, key=lambda x: x.BurstTime)
            process_list.remove(process)
            start_time = time
            end_time = time + process.BurstTime
            process_times.append((process.pid, start_time, end_time))
            time = end_time
        else:
            time += 1

    return process_times

def SRTF(process_list):
    time = 0
    process_queue = []
    process_times = []

    while process_list or process_queue:
        while process_list and process_list[0].ArrivalTime <= time:
            process_queue.append(process_list.pop(0))

        if process_queue:
            process_queue.sort(key=lambda x: x.RemainingTime)
            process = process_queue[0]
            process.RemainingTime -= 1
            start_time = time
            time += 1

            if process.RemainingTime == 0:
                end_time = time
                process_queue.remove(process)
                process_times.append((process.pid, start_time, end_time))
        else:
            time += 1

    return process_times

def priority(process_list):
    time = 0
    process_times = []

    while process_list:
        available = [p for p in process_list if p.ArrivalTime <= time]
        if available:
            process = min(available, key=lambda x: x.Priority)
            process_list.remove(process)
            start_time = time
            end_time = time + process.BurstTime
            process_times.append((process.pid, start_time, end_time))
            time = end_time
        else:
            time += 1

    return process_times

def round_robin(process_list, time_quanta):
    time = 0
    process_queue = []
    process_times = []

    while process_list or process_queue:
        while process_list and process_list[0].ArrivalTime <= time:
            process_queue.append(process_list.pop(0))

        if process_queue:
            process = process_queue.pop(0)
            start_time = time
            quantum = min(time_quanta, process.RemainingTime)
            process.RemainingTime -= quantum
            time += quantum

            if process.RemainingTime == 0:
                end_time = time
                process_times.append((process.pid, start_time, end_time))
            else:
                process_queue.append(process)
        else:
            time += 1

    return process_times

class SchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms")
        self.root.geometry("1200x600")
        self.root.resizable(False, False)
        self.process_list = []
        self.selected_algorithm = ctk.StringVar(value="FCFS")
        self.error_label = None
        self.setup_welcome_page()

    def setup_welcome_page(self):
        """Setup the welcome page with an image and button."""
        self.welcome_frame = ctk.CTkFrame(self.root)
        self.welcome_frame.pack(fill=ctk.BOTH, expand=True)

        # Load the image (replace with your image path)
        image_path = "C:/Users/moham/Desktop/Operating System/Sub Project/Yonis.png"
        image = Image.open(image_path)
        image = image.resize((500, 400))
        img = ImageTk.PhotoImage(image)

        # Display image
        self.image_label = ctk.CTkLabel(self.welcome_frame, image=img, text="")
        self.image_label.image = img  # Keep reference to prevent garbage collection
        self.image_label.pack(pady=20)

        # Welcome message
        welcome_message = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to the CPU Scheduling App",
            font=("Helvetica", 20, "bold"),
        )
        welcome_message.pack(pady=10)

        # Open App Button
        open_app_button = ctk.CTkButton(
            self.welcome_frame,
            text="Open Application",
            font=("Helvetica", 16, "bold"),
            command=self.open_main_app,
        )
        open_app_button.pack(pady=20)

    def open_main_app(self):
        """Destroy the welcome page and open the main app."""
        self.welcome_frame.destroy()
        self.setup_ui()

    def setup_ui(self):
        """Setup the main application interface."""
        left_frame = ctk.CTkFrame(self.root, width=200, corner_radius=12)
        left_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)
        left_frame.pack_propagate(False)

        right_frame = ctk.CTkFrame(self.root, width=500, corner_radius=12)
        right_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)
        right_frame.pack_propagate(False)

        bottom_frame = ctk.CTkFrame(self.root, height=500, width=600, corner_radius=12)
        bottom_frame.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=10, pady=10)

        ctk.CTkLabel(left_frame, text="Add Process", font=("Helvetica", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(left_frame, text="Process ID:").pack(anchor=ctk.W, pady=5)
        self.pid_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Process ID")
        self.pid_entry.pack(fill=ctk.X, pady=5)

        ctk.CTkLabel(left_frame, text="Burst Time:").pack(anchor=ctk.W, pady=5)
        self.burst_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Burst Time", width=10)
        self.burst_entry.pack(fill=ctk.X, pady=5)

        ctk.CTkLabel(left_frame, text="Arrival Time:").pack(anchor=ctk.W, pady=5)
        self.arrival_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Arrival Time")
        self.arrival_entry.pack(fill=ctk.X, pady=5)

        ctk.CTkLabel(left_frame, text="Priority (if required):").pack(anchor=ctk.W, pady=5)
        self.priority_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Priority (optional)")
        self.priority_entry.pack(fill=ctk.X, pady=5)

        ctk.CTkLabel(left_frame, text="Time Quantum (if required):").pack(anchor=ctk.W, pady=5)
        self.quantum_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Time Quantum (optional)")
        self.quantum_entry.pack(fill=ctk.X, pady=5)

        ctk.CTkButton(left_frame, text="Add Process", command=self.add_process).pack(pady=10, fill=ctk.X)

        # Error Label
        self.error_label = ctk.CTkLabel(left_frame, text="", text_color="red", wraplength=260)
        self.error_label.pack(pady=5)

        ctk.CTkLabel(right_frame, text="Process List", font=("Helvetica", 30, "bold")).pack(pady=10)
        self.process_tree = ttk.Treeview(right_frame, columns=("PID", "Burst", "Arrival", "Priority"), show="headings")
        self.process_tree.heading("PID", text="Process ID")
        self.process_tree.heading("Burst", text="Burst Time")
        self.process_tree.heading("Arrival", text="Arrival Time")
        self.process_tree.heading("Priority", text="Priority")
        self.process_tree.pack(fill=ctk.BOTH, padx=10, pady=10)

        ctk.CTkLabel(right_frame, text="Select Algorithm", font=("Helvetica", 18, "bold")).pack(pady=10)
        algorithms = [("First-Come First-Served (FCFS)", "FCFS"), ("Shortest Job First (SJF)", "SJF"),
                      ("Shortest Remaining Time First (SRTF)", "SRTF"), ("Priority Scheduling", "Priority"),
                      ("Round Robin (RR)", "Round Robin")]

        for text, value in algorithms:
            ctk.CTkRadioButton(right_frame, text=text, variable=self.selected_algorithm, value=value).pack(anchor=ctk.W, padx=10, pady=5)

        ctk.CTkButton(right_frame, text="Run Algorithm", command=self.run_algorithm).pack(pady=10, fill=ctk.X)

        self.gantt_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
        self.gantt_frame.pack(fill=ctk.BOTH, expand=True)

    def add_process(self):
        pid = self.pid_entry.get().strip()
        burst = self.burst_entry.get().strip()
        arrival = self.arrival_entry.get().strip()
        priority = self.priority_entry.get().strip() or 0
        if not pid or not burst.isdigit() or not arrival.isdigit():
            self.show_error("Please provide valid inputs for Process ID, Burst Time, and Arrival Time.")
            return
        if priority and not priority.isdigit():
            self.show_error("Priority must be a valid integer.")
            return
        self.process_list.append(ProcessAttributes(pid, int(burst), int(arrival), int(priority)))
        self.process_tree.insert("", "end", values=(pid, burst, arrival, priority))
        self.clear_inputs()

    def run_algorithm(self):
        algorithm = self.selected_algorithm.get()
        if algorithm == "Priority":
            process_times = priority(self.process_list.copy())
        elif algorithm == "Round Robin":
            quantum = self.quantum_entry.get().strip()
            if not quantum.isdigit() or int(quantum) <= 0:
                self.show_error("Time Quantum must be a positive integer.")
                return
            process_times = round_robin(self.process_list.copy(), int(quantum))
        elif algorithm == "FCFS":
            process_times = FCFS(self.process_list.copy())
        elif algorithm == "SJF":
            process_times = SJF(self.process_list.copy())
        elif algorithm == "SRTF":
            process_times = SRTF(self.process_list.copy())
        else:
            self.show_error("Please select a valid algorithm.")
            return
        self.clear_error()
        self.plot_gantt_chart(process_times, algorithm)

    def plot_gantt_chart(self, process_times, name):
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()
        fig = plt.figure(figsize=(10, 6))  # Larger height
        ax = fig.add_subplot(111)
        colors = ['#4CAF50', '#2196F3', '#FF5722', '#9C27B0', '#FFEB3B', '#00BCD4']

        y_position = 10  # Fixed vertical position
        height = 8 
        for i, (pid, start_time, end_time) in enumerate(process_times):
            ax.broken_barh([(start_time, end_time - start_time)], (y_position, height), facecolors=colors[i % len(colors)])
            ax.text(start_time + (end_time - start_time) / 2, y_position + height / 2, pid, ha='center', va='center', fontsize=9, color='white')

        ax.set_xlim(0, max([end for _, _, end in process_times]) + 1)
        ax.set_ylim(0, y_position + height + 10)
        ax.set_xlabel("Time")
        ax.set_title(f"Gantt Chart for {name} Scheduling")
        
        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=ctk.BOTH)
        canvas.draw()

    def show_error(self, message):
        self.error_label.configure(text=message)

    def clear_error(self):
        self.error_label.configure(text="")

    def clear_inputs(self):
        self.pid_entry.delete(0, ctk.END)
        self.burst_entry.delete(0, ctk.END)
        self.arrival_entry.delete(0, ctk.END)
        self.priority_entry.delete(0, ctk.END)
        self.quantum_entry.delete(0, ctk.END)


if __name__ == "__main__":
    root = ctk.CTk()
    app = SchedulingApp(root)
    root.mainloop()
