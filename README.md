# Network Monitoring & Health Check Tool
### Python + Socket Programming | No External Libraries

A Python-based network monitoring tool that checks device 
connectivity, measures network latency, and scans TCP port 
availability using raw socket programming.

---

## Features
- Connectivity check using TCP socket connection
- Latency measurement with average over multiple attempts
- TCP port availability scanning using threads
- Automatic log file generation with timestamps
- Health report saved to file after every run

---

## Tech Stack
| Tool            | Purpose                              |
|-----------------|--------------------------------------|
| Python 3.13     | Core language                        |
| socket          | TCP connectivity and port scanning   |
| threading       | Parallel port scanning for speed     |
| logging         | Timestamped log file generation      |
| datetime        | Report and log file naming           |

No external libraries needed — pure Python built-ins only!

---

## Project Structure
| File              | Purpose                              |
|-------------------|--------------------------------------|
| monitor.py        | Main script — runs all checks        |
| health_check.py   | Connectivity and latency functions   |
| port_scanner.py   | Multi-threaded TCP port scanner      |
| logger.py         | Logging configuration                |
| targets.py        | List of devices to monitor           |

---

## Sample Output