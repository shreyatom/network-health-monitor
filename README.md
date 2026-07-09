# network-health-monitor

A Python tool I built to monitor network device health — checking
connectivity, measuring latency, and scanning TCP ports using only
Python's built-in socket module. No external libraries required.

---

## Why I Built This

Manual network health checks are slow and error-prone. This tool
automates the process — run one script and get a full report of
which devices are up, how fast they respond, and which ports are
open.

---

## What It Does

- Connects to each target device using raw TCP sockets
- Measures response latency (average of 3 attempts)
- Scans specified TCP ports and reports open/closed status
- Logs all activity with timestamps to a file in logs/
- Saves a full health report to reports/ after every run

---

## Project Structure

network-health-monitor/
├── monitor.py          entry point — run this
├── health_check.py     connectivity and latency logic
├── port_scanner.py     threaded port scanner
├── logger.py           logging setup
├── targets.py          devices and ports to monitor
├── logs/               auto-created, stores .log files
└── reports/            auto-created, stores health reports

---

## How to Run

Clone the repo:

git clone https://github.com/shreyatom/network-health-monitor.git
cd network-health-monitor

Add your devices in targets.py:

TARGETS = [
    {
        'name':  'Core Router',
        'host':  '192.168.1.1',
        'ports': [22, 80, 443],
    },
]

Run:

python monitor.py

Check the reports/ folder for the full output.

---

## Sample Output

HEALTH CHECK SUMMARY
=====================================================
Device               Status    Latency      Ports
-----------------------------------------------------
Google DNS           UP        66.7 ms      53:O, 443:O
Cloudflare DNS       UP        87.9 ms      53:O, 443:O
-----------------------------------------------------
Result: 2/2 devices reachable

---

## Things I Learned Building This

- How TCP sockets work at the code level using AF_INET and SOCK_STREAM
- Why connect_ex() is better than connect() for port scanning
- How threading speeds up port scans and why locks prevent race conditions
- The difference between logging to file vs printing to terminal
- How to measure network latency using time.time() in Python

---

## Built With

Python 3.13 — standard library only
socket, threading, logging, datetime, os, sys, time