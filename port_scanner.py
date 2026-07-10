"""port_scanner.py
Scans multiple ports on multiple devices simultaneously
using Python threading for speed.
"""

import socket
import threading
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import logger
from targets import COMMON_PORTS

# store scan results
scan_results = {}
results_lock = threading.Lock()  # prevents two threads writing at same time

def scan_port(host, port, timeout=3):
    """Scans one port on one host, runs in its own thread."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        # get port name or use number
        port_name = COMMON_PORTS.get(port, str(port))
        status = 'OPEN' if result == 0 else 'CLOSED'

        # thread-safe write
        with results_lock:
            if host not in scan_results:
                scan_results[host] = {}
            scan_results[host][port] = {
                'status':    status,
                'port_name': port_name,
            }

        if result == 0:
            logger.info(f"SCAN | {host:<20} | Port {port:<6} ({port_name:<10}) | OPEN")
        else:
            logger.info(f"SCAN | {host:<20} | Port {port:<6} ({port_name:<10}) | CLOSED")

    except Exception as e:
        logger.error(f"SCAN ERROR | {host} | Port {port} | {e}")

def scan_ports_threaded(host, ports):
    """Scans all ports on host simultaneously using threads."""
    logger.info(f"Starting port scan on {host} — {len(ports)} ports")

    threads = []

    # create one thread per port
    for port in ports:
        thread = threading.Thread(
            target=scan_port,
            args=(host, port)
        )
        threads.append(thread)
        thread.start()  # start thread immediately

    # wait for all threads
    for thread in threads:
        thread.join()

    logger.info(f"Port scan complete on {host}")
    return scan_results.get(host, {})

def scan_all_targets(targets):
    """Scans all devices and ports. Returns complete results dict."""
    print("\n" + "="*55)
    print("PORT SCANNER STARTING")
    print("="*55)

    all_results = {}

    for target in targets:
        name  = target['name']
        host  = target['host']
        ports = target['ports']

        print(f"\nScanning {name} ({host})...")
        results = scan_ports_threaded(host, ports)
        all_results[name] = {
            'host':    host,
            'ports':   results
        }

    print("\n" + "="*55)
    print("PORT SCAN COMPLETE")
    print("="*55)

    return all_results