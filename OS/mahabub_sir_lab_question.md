## CIT-322: Operating Systems Sessional Laboratory 
**Department of CSIT, CSE, PSTU** 
This document outlines the comprehensive weekly distribution for the Operating Systems Lab.

---

### Module 1: Interface and Environment
**Week 1: Multi-OS Shell & Scripting** 
* **Linux**: Focus on Bash scripting, file permissions (`chmod`), and piping(|).
* **Windows**: Focus on PowerShell scripting, Windows Registry basics, and Environment Variables.
* **Task**: Write a cross-platform report comparing `ls` vs `dir` and `grep` vs `Select-String`.

---

### Module 2: Process Management 
**Week 2: Process Control - System Calls (Part I)** 
* **Linux**: Creating processes using `fork()`, `exec()`, and `wait()`.
* **Windows**: Creating processes using the `CreateProcess()` API in C++.
* **Task**: Observe "Zombie" processes in Linux and "Background Processes" in Windows Task Manager.

**Week 3: Process Control - System Calls (Part II)**
* **Linux**: Handling signals (`SIGKILL`, `SIGINT`) using `signal.h`.
* **Windows**: Process termination and priority manipulation via `SetPriorityClass`.
* **Task**: Build a "Mini-Shell" that executes commands and handles `Ctrl+C` gracefully.

---

### Module 3: CPU Scheduling
**Week 4: Non-Preemptive Scheduling**
* **Algorithms**: First-Come-First-Served (FCFS) and Shortest Job First (SJF).
* **Task**: Write a simulator to calculate Average Waiting Time (AWT) and Turnaround Time (TAT).

**Week 5: Preemptive Scheduling** [cite: 26]
* **Algorithms**: Round Robin (RR) and Shortest Remaining Time First (SRTF)[cite: 27].
* **Task**: Simulate a Multi-level Queue scheduler where interactive jobs have higher priority.

---

### Module 4: Synchronization & IPC 
**Week 6: Inter-Process Communication (IPC)** 
* **Linux**: Anonymous Pipes and Named Pipes (FIFOs).
* **Windows**: Windows Mailslots or Named Pipes.
* **Task**: Implement a client-server chat using shared memory.

**Week 7: Threading & Synchronization (Part I)** 
* **Tools**: POSIX Threads (`pthreads`) vs Windows Threads (`CreateThread`).
* **Concept**: Solving Race Conditions using Mutexes and Semaphores.
* **Task**: The Classic Producer-Consumer Problem.

**Week 8: Synchronization (Part II)** 
* **Advanced Problems**: The Dining Philosophers and Readers-Writers problems.
* **Task**: Use a "Deadlock Detector" tool or manual code analysis to find circular waits.

---

### Module 5: Memory Management 
**Week 9: Memory Allocation Strategies** 
* **Task**: Simulate First-Fit, Best-Fit, and Worst-Fit allocation in a fixed-size memory block.
* **Analysis**: Measure Internal vs. External Fragmentation.

**Week 10: Virtual Memory & Paging** 
* **Algorithms**: FIFO, LRU (Least Recently Used), and Optimal Page Replacement.
* **Task**: Calculate "Page Faults" for a given reference string.

---

### Module 6: Storage & Security 
**Week 11: File System Management** 
* **Concepts**: Inodes (Linux) vs File Allocation Table/MFT (Windows).
* **Task**: Create a program to traverse a directory recursively and list file metadata (size, owner, timestamps).

**Week 12: Disk Scheduling** 
* **Algorithms**: FCFS, SSTF, SCAN, C-SCAN.
* **Task**: Visualize the disk head movement path for a sequence of track requests.

---

### Module 7: Final Integration 
**Week 13: System Security & Protection** 
* **Linux**: Implementing Access Control Lists (ACL).
* **Windows**: Managing User Accounts and Permissions via PowerShell.

**Week 14: Capstone Project Lab** 
* **Project Choice A**: Build a "System Monitor" (like a CLI-based Task Manager).
* **Project Choice B**: Implement a simplified Virtual File System (VFS).
* **Project Choice C**: Implement a Linux Kernel.
