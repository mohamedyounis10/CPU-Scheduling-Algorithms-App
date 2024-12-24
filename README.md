# CPU Scheduling Algorithms

This repository contains two main components:

1. **CPU Scheduling Algorithms**: Core implementations of CPU scheduling algorithms (without UI).
2. **CPU Scheduling App with UI**: An interactive application for visualizing and running CPU scheduling algorithms, combining both the algorithms and a graphical user interface (GUI).

---

## Features

- **Supported Algorithms**:
  - First-Come First-Served (FCFS)
  - Shortest Job First (SJF)
  - Shortest Remaining Time First (SRTF)
  - Priority Scheduling
  - Round Robin (RR)
- **Interactive UI**:
  - Add processes dynamically.
  - Visualize the Gantt Chart for each scheduling algorithm.
  - Error handling for invalid inputs.
- **Standalone Core Algorithms**:
  - The `cpu_scheduling_algorithms.py` file contains the core implementations of scheduling algorithms, independent of the GUI.
- **Integrated Application**:
  - The `cpu_scheduling_app.py` file combines the algorithms and an interactive UI in a single application.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mohamedyounis10/cpu-scheduling-app.git
   cd cpu-scheduling-app
   ```
2. Install dependencies:
   ```bash
   pip install customtkinter matplotlib pillow
   ```
3. Run the GUI application:
   ```bash
   python cpu_scheduling_app.py
   ```

---

## Screenshots

### Welcome Screen

![Screenshot 2024-12-24 205248](https://github.com/user-attachments/assets/83972a16-a743-4a87-ada7-34bcf02b60c8)


### Main Application Interface

![image](https://github.com/user-attachments/assets/cf45781d-6743-4c2e-9c6e-01592a5fff35)


---

## Usage

### **Core Algorithm Usage**

You can use the core algorithms independently by importing them from the `cpu_scheduling_algorithms.py` file. Example:

```python
from cpu_scheduling_algorithms import FCFS, ProcessAttributes

processes = [
    ProcessAttributes(pid="P1", BurstTime=5, ArrivalTime=0),
    ProcessAttributes(pid="P2", BurstTime=3, ArrivalTime=2),
    ProcessAttributes(pid="P3", BurstTime=8, ArrivalTime=4),
]

result = FCFS(processes)
print(result)  # Output: [("P1", 0, 5), ("P2", 5, 8), ("P3", 8, 16)]
```

### **GUI Usage**

1. Launch the application and add processes by filling out the fields for Process ID, Burst Time, Arrival Time, and optionally Priority/Time Quantum.
2. Select a scheduling algorithm.
3. Click "Run Algorithm" to visualize the Gantt Chart.

---

## Files

- **cpu\_scheduling\_app.py**: The main file for the GUI application that combines the scheduling algorithms and an interactive UI.
- **cpu\_scheduling\_algorithms.py**: Contains core implementations of scheduling algorithms, designed to be used independently of any GUI.
- **images/**: Directory for screenshots and other assets.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements or report bugs.

---

## Author

Created by [Mohamed Younis](https://github.com/mohamedyounis10).

