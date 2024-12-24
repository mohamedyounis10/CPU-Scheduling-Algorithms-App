# Library Use It in Draw Gantt Chart
import matplotlib.pyplot as plt

# Class Have Atrributes of Process 
class ProcessAttributes:
    def __init__(self, pid, BurstTime, ArrivalTime, Priority=0, WaitingTime=0, TurnAroundTime=0):
        self.pid = pid
        self.BurstTime = BurstTime
        self.ArrivalTime = ArrivalTime
        self.Priority = Priority
        self.WaitingTime = WaitingTime
        self.TurnAroundTime = TurnAroundTime
        self.RemainingTime = BurstTime  # To track remaining time for preemptive scheduling

    def __str__(self):
        return f"ProcessAttributes(pid={self.pid}, BurstTime={self.BurstTime}, ArrivalTime={self.ArrivalTime}, RemainingTime={self.RemainingTime}, WaitingTime={self.WaitingTime}, TurnAroundTime={self.TurnAroundTime}, Priority={self.Priority})"

# First-Come First-Served Scheduling
def FCFS(process_list):
    time = 0
    gantt = []  # Store Gantt chart data
    completed = {}  # Store completed processes data (end time, turnaround time, waiting time)
    process_list.sort(key=lambda x: x.ArrivalTime)  # Sort by Arrival Time
    
    total_waiting_time = 0
    total_turnaround_time = 0

    # Collect start time and end time for Gantt chart
    process_times = []
    original_length = len(process_list)  # Store the original length

    while process_list:
        if process_list[0].ArrivalTime > time:
            gantt.append("Idle")  # If no process is available, mark idle
            time += 1
            continue
        else:
            process = process_list.pop(0)  # Take the first process that has arrived
            gantt.append(process.pid)
            start_time = time
            end_time = time + process.BurstTime
            time = end_time
            process_times.append((process.pid, start_time, end_time))
            
            # Calculate turnaround time and waiting time
            turnaround_time = end_time - process.ArrivalTime
            waiting_time = turnaround_time - process.BurstTime
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
            completed[process.pid] = [end_time, turnaround_time, waiting_time]
            
    average_waiting_time = total_waiting_time / original_length
    average_turnaround_time = total_turnaround_time / original_length

    print("FCFS:", gantt)
    print(completed)
    print("Average Waiting Time: ",average_waiting_time)
    print("Average Turnaround Time:",average_turnaround_time)
    return process_times

# Shortest Job First Scheduling Non Preemptive
def SJF(process_list):
    time = 0
    gantt = []  
    completed = {}
    process_list.sort(key=lambda x: x.ArrivalTime)  # lambada : this function take one argument and Sort by Arrival Time

    total_waiting_time = 0
    total_turnaround_time = 0

    # Collect start time and end time for Gantt chart
    process_times = []
    original_length = len(process_list) 

    while process_list:
        # Filter processes that have arrived by the current time
        available_processes = []
        for i in process_list:
            if i.ArrivalTime <= time:
                available_processes.append(i)
        
        if available_processes:
            # Choose the process with the shortest burst time
            process = min(available_processes, key=lambda x: x.BurstTime)
            process_list.remove(process)
            
            gantt.append(process.pid)
            start_time = time
            end_time = time + process.BurstTime
            time = end_time
            process_times.append((process.pid, start_time, end_time))
            
            # Calculate turnaround time and waiting time
            turnaround_time = end_time - process.ArrivalTime
            waiting_time = turnaround_time - process.BurstTime
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
            completed[process.pid] = [end_time, turnaround_time, waiting_time]
        else:
            # If no process has arrived, increment time and add idle
            gantt.append("Idle")
            time += 1

    average_waiting_time = total_waiting_time / original_length
    average_turnaround_time = total_turnaround_time / original_length

    print("SJF:", gantt)
    print(completed)
    print("Average Waiting Time: ",average_waiting_time)
    print("Average Turnaround Time:",average_turnaround_time)
    return process_times

# Shortest Remaining Time First 
def SRTF(process_list):
    time = 0
    gantt = [] 
    completed = {} 
    process_list.sort(key=lambda x: x.ArrivalTime)  # Sort by Arrival Time

    # List to store processes that are waiting to be scheduled
    process_queue = []
    process_times = []

    total_waiting_time = 0
    total_turnaround_time = 0
    original_length = len(process_list)  # Store the original length 

    while process_list or process_queue:
        # Add all processes that have arrived by the current time to the queue
        while process_list and process_list[0].ArrivalTime <= time:
            process_queue.append(process_list.pop(0))

        if process_queue:
            # Select the process with the shortest remaining burst time
            process_queue.sort(key=lambda x: x.RemainingTime)  # Sort by Remaining Time
            process = process_queue[0]

            gantt.append(process.pid)
            start_time = time
            time += 1  # Process runs for 1 unit of time (preemptive)
            process.RemainingTime -= 1

            # If process is completed, calculate turnaround and waiting time
            if process.RemainingTime == 0:
                end_time = time
                turnaround_time = end_time - process.ArrivalTime
                waiting_time = turnaround_time - process.BurstTime
                total_waiting_time += waiting_time
                total_turnaround_time += turnaround_time
                completed[process.pid] = [end_time, turnaround_time, waiting_time]

                # Record the process completion in the process_times list
                process_times.append((process.pid, start_time, end_time))
                process_queue.remove(process)  # Remove completed process
        else:
            # No process is ready to run, so idle
            gantt.append("Idle")
            time += 1

    average_waiting_time = total_waiting_time / original_length
    average_turnaround_time = total_turnaround_time / original_length

    print(f"SRTF Gantt Chart: {gantt}")
    print(f"SRTF Completed Processes Data: {completed}")
    print("Average Waiting Time: ",average_waiting_time)
    print("Average Turnaround Time:",average_turnaround_time)
    return process_times

# Priority Scheduling Non Preemptive
def priority(process_list):
    time = 0
    gantt = []  
    completed = {}  
    process_times = []

    total_waiting_time = 0
    total_turnaround_time = 0
    original_length = len(process_list)  # Store the original length 
    
    while process_list:
        # Create a copy of the process list to avoid modification issues
        available_processes = process_list.copy() 
        
        if available_processes:
            # Choose the process with the highest priority (lowest value)
            process = min(available_processes, key=lambda x: x.Priority)
            process_list.remove(process)  # Remove the selected process from the original list
            
            # Record start time for the process
            start_time = time
            gantt.append(process.pid)
            
            # Process runs for its burst time
            time += process.BurstTime
            process.RemainingTime = 0  # Process completes
            
            # Calculate end time
            end_time = time
            turnaround_time = end_time - process.ArrivalTime
            waiting_time = turnaround_time - process.BurstTime
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
            completed[process.pid] = [end_time, turnaround_time, waiting_time]
            
            # Record the process completion in the process_times list
            process_times.append((process.pid, start_time, end_time))
        else:
            # No process is ready to run, so idle
            gantt.append("Idle")
            time += 1

    average_waiting_time = total_waiting_time / original_length
    average_turnaround_time = total_turnaround_time / original_length

    print(f"Priority Gantt Chart: {gantt}")
    print(f"Priority Completed Processes Data: {completed}")
    print("Average Waiting Time: ",average_waiting_time)
    print("Average Turnaround Time:",average_turnaround_time)
    return process_times

# Round Robin Scheduling Preemptive
def round_robin(process_list, time_quanta):
    time = 0
    gantt = []  
    completed = {}  # Store completed processes data (end time, turnaround time, waiting time)
    process_times = []
    
    # Sort the processes by Arrival Time
    process_list.sort(key=lambda x: x.ArrivalTime)

    # Create a queue for processes
    queue = []

    total_waiting_time = 0
    total_turnaround_time = 0
    original_length = len(process_list)  # Store the original length of the process list for average calculation

    while process_list or queue:
        # Add all processes that have arrived by the current time to the queue
        while process_list and process_list[0].ArrivalTime <= time:
            queue.append(process_list.pop(0))

        if queue:
            process = queue.pop(0)
            start_time = time  # Record the start time
            gantt.append(process.pid)

            if process.RemainingTime <= time_quanta:
                time += process.RemainingTime
                process.RemainingTime = 0
                end_time = time
                turnaround_time = end_time - process.ArrivalTime
                waiting_time = turnaround_time - process.BurstTime
                total_waiting_time += waiting_time
                total_turnaround_time += turnaround_time
                completed[process.pid] = [end_time, turnaround_time, waiting_time]
                process_times.append((process.pid, start_time, end_time))
            else:
                time += time_quanta
                process.RemainingTime -= time_quanta
                end_time = time
                queue.append(process)  # Re-queue the process

                # Store intermediate process times for Gantt chart
                process_times.append((process.pid, start_time, end_time))
        else:
            # No process is ready to run, so idle
            gantt.append("Idle")
            time += 1

    average_waiting_time = total_waiting_time / original_length
    average_turnaround_time = total_turnaround_time / original_length

    print("Round Robin Gantt Chart: ",gantt)
    print("Round Robin Completed Data: ",completed)
    print(f"Average Waiting Time: {average_waiting_time}")
    print(f"Average Turnaround Time: {average_turnaround_time}")
    return process_times

# Function to show Gantt Chart
def plot_gantt_chart(name, process_times):
    plt.figure(name, figsize=(8, 4))  # Create a figure with specific size
    
    # Define a list of colors for each process
    colors = ['#4CAF50', '#2196F3', '#FF5722', '#9C27B0', '#FFEB3B', '#00BCD4']
    
    # Create bars for each process
    for i, (pid, start_time, end_time) in enumerate(process_times):
        color = colors[i % len(colors)]  # Assign a color to each process, cycling through the colors
        bar_width = end_time - start_time
        plt.barh(0, bar_width, left=start_time, color=color)  # Plot all in the same row (y=0)
        
        # Add the process ID (P1, P2, etc.) on top of the bars
        plt.text(start_time + bar_width / 2, 0, pid, ha='center', va='center', color='white', fontsize=12)
    
    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title(f'Gantt Chart for {name} Scheduling')
    
    # Set xticks to represent time intervals more clearly
    plt.xticks(range(0, max([end for _, _, end in process_times]) + 1))
    
    # Set y-axis limits to start from 0 and end at a small offset, since all bars are in the same row
    plt.ylim(-0.5, 0.5)
    
    # Display the chart
    plt.show()

if __name__ == "__main__":
    name = ''
    process_list = []
    print('Process : ')
    number_process = int(input('Enter number of precess : '))
    for i in range (number_process):
        uid = input('Enter name of process : ')
        burst = int(input('Enter number of Brust time : '))
        Arrival = int(input('Enter number of arival time : '))
        print('-'*10)
        process_list.append(ProcessAttributes(uid,burst,Arrival))

    while True:
        print('-'*10)
        print("Select the scheduling algorithm to run:")
        print("1. First-Come First-Served (FCFS)")
        print("2. Shortest Job First (SJF)")
        print("3. Shortest Remaining Time First (SRTF)")
        print("4. Priority Scheduling (Non-Preemptive)")
        print("5. Round Robin Scheduling")
        print("6. Exit")
        print('-'*10)
        choice = int(input("Enter your choice: "))

        if choice == 6:
            print('Thank You')
            break

        if choice in [1, 2, 3, 4, 5]:
            if choice == 1:
                name = 'FCFS'
                process_times = FCFS(process_list.copy())
            elif choice == 2:
                name = 'SJF'
                process_times = SJF(process_list.copy())
            elif choice == 3:
                name = 'SRTF'
                process_times = SRTF(process_list.copy())
            elif choice == 4:
                name = 'Priority'
                # Priority Scheduling requires priorities to be set
                for process in process_list:
                    process.Priority = int(input(f"Enter priority for process {process.pid}: "))
                process_times = priority(process_list.copy())
            elif choice == 5:
                name = 'Round Robin'
                time_quanta = int(input("Enter time quantum for Round Robin Scheduling: "))
                process_times = round_robin(process_list.copy(), time_quanta)

            plot_gantt_chart(name,process_times)

        else:
            print("Invalid choice. Please try again.")
        
