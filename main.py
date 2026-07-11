"""monitor.py
Main script — runs all health checks and generates report.
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import logger
from targets import TARGETS
from health_check import check_connectivity, check_port, measure_latency
from port_scanner import scan_all_targets

def run_health_checks():
    """Checks all targets and returns results."""
    print("\n" + "="*55)
    print("NETWORK HEALTH CHECK STARTING")
    print("="*55)

    results = []

    for target in TARGETS:
        name  = target['name']
        host  = target['host']
        ports = target['ports']

        print(f"\nChecking {name} ({host})...")
        logger.info(f"{'='*40}")
        logger.info(f"Checking: {name} ({host})")

        # reachable?
        is_reachable, latency = check_connectivity(host)

        # avg latency
        avg_latency = None
        if is_reachable:
            avg_latency = measure_latency(host, ports[0])

        # port scan
        port_results = {}
        for port in ports:
            is_open = check_port(host, port)
            port_results[port] = is_open

        # store results
        results.append({
            'name':        name,
            'host':        host,
            'reachable':   is_reachable,
            'latency_ms':  avg_latency,
            'ports':       port_results,
            'timestamp':   datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })

    return results

def generate_report(health_results, scan_results):
    """Creates health report and saves to reports/ folder."""
    timestamp   = datetime.now().strftime('%Y%m%d_%H%M')
    filename    = f"reports/health_report_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f: 
        # header
        f.write("="*60 + "\n")
        f.write("NETWORK HEALTH REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")

        # health check results
        f.write("CONNECTIVITY & LATENCY\n")
        f.write("-"*60 + "\n")

        reachable_count = 0
        for r in health_results:
            status = "REACHABLE" if r['reachable'] else "UNREACHABLE"
            if r['reachable']:
                reachable_count += 1

            f.write(f"\nDevice:    {r['name']} ({r['host']})\n")
            f.write(f"Status:    {status}\n")
            f.write(f"Latency:   {r['latency_ms']} ms\n" if r['latency_ms'] else "Latency:   N/A\n")
            f.write(f"Checked:   {r['timestamp']}\n")

            # port results
            f.write("Ports:\n")
            for port, is_open in r['ports'].items():
                port_status = "OPEN" if is_open else "CLOSED"
                f.write(f"  Port {port}: {port_status}\n")

        # summary
        f.write("\n" + "="*60 + "\n")
        f.write("SUMMARY\n")
        f.write("-"*60 + "\n")
        f.write(f"Total devices checked: {len(health_results)}\n")
        f.write(f"Reachable:             {reachable_count}\n")
        f.write(f"Unreachable:           {len(health_results) - reachable_count}\n")

        # port scan results
        f.write("\nPORT SCAN RESULTS\n")
        f.write("-"*60 + "\n")
        for device_name, data in scan_results.items():
            f.write(f"\n{device_name} ({data['host']})\n")
            for port, info in data['ports'].items():
                f.write(f"  Port {port} ({info['port_name']}): {info['status']}\n")

    logger.info(f"Report saved: {filename}")
    print(f"\nReport saved: {filename}")
    return filename

def print_summary(results):
    """Prints summary table to terminal."""
    print("\n" + "="*55)
    print("HEALTH CHECK SUMMARY")
    print("="*55)
    print(f"{'Device':<20} {'Status':<15} {'Latency':<12} {'Ports'}")
    print("-"*55)

    for r in results:
        status  = "UP" if r['reachable'] else "DOWN"
        latency = f"{r['latency_ms']} ms" if r['latency_ms'] else "N/A"
        ports   = ", ".join([
            f"{p}:{'O' if s else 'X'}"
            for p, s in r['ports'].items()
        ])
        print(f"{r['name']:<20} {status:<15} {latency:<12} {ports}")

    reachable = sum(1 for r in results if r['reachable'])
    print("-"*55)
    print(f"Result: {reachable}/{len(results)} devices reachable")


# main
if __name__ == '__main__':
    print("\n" + "="*55)
    print(" NETWORK MONITORING & HEALTH CHECK TOOL")
    print(" Python + Socket Programming")
    print("="*55)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Monitoring {len(TARGETS)} devices")
    print("="*55)

    # Step 1: health checks
    health_results = run_health_checks()

    # Step 2: port scanner
    scan_results = scan_all_targets(TARGETS)

    # Step 3: summary
    print_summary(health_results)

    # Step 4: report
    generate_report(health_results, scan_results)

    print("\nDone! Check reports/ folder for full report.")