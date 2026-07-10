"""health_check.py
Checks device connectivity, latency, and port availability
using Python's built-in socket library.
No external libraries needed — pure Python!
"""

import socket
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import logger

def check_connectivity(host, timeout=3):
    """Checks if host is reachable via TCP. Returns (is_reachable, latency_ms)."""
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, 80))
        sock.close()
        end_time = time.time()

        # calculate latency_ms
        latency_ms = round((end_time - start_time) * 1000, 2)

        if result == 0:
            logger.info(f"REACHABLE   | {host:<20} | Latency: {latency_ms} ms")
            return True, latency_ms
        else:
            # try port 443 if 80 failed
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.settimeout(timeout)
            result2 = sock2.connect_ex((host, 443))
            sock2.close()

            end_time2 = time.time()
            latency_ms2 = round((end_time2 - start_time) * 1000, 2)

            if result2 == 0:
                logger.info(f"REACHABLE   | {host:<20} | Latency: {latency_ms2} ms")
                return True, latency_ms2
            else:
                logger.warning(f"UNREACHABLE | {host:<20} | No response")
                return False, None

    except socket.timeout:
        logger.warning(f"TIMEOUT     | {host:<20} | No response in {timeout}s")
        return False, None

    except socket.gaierror:
        logger.error(f"DNS ERROR   | {host:<20} | Could not resolve hostname")
        return False, None

    except Exception as e:
        logger.error(f"ERROR       | {host:<20} | {e}")
        return False, None


def check_port(host, port, timeout=3):
    """True if port is open, False if closed."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # connect_ex: 0 = open, nonzero = closed
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            logger.info(f"PORT OPEN   | {host:<20} | Port {port}")
            return True
        else:
            logger.warning(f"PORT CLOSED | {host:<20} | Port {port}")
            return False

    except socket.timeout:
        logger.warning(f"PORT TIMEOUT| {host:<20} | Port {port}")
        return False

    except Exception as e:
        logger.error(f"PORT ERROR  | {host:<20} | Port {port} | {e}")
        return False

def measure_latency(host, port=443, attempts=3):
    """Average latency over multiple pings (ms), or None if unreachable."""

    latencies = []

    for i in range(attempts):
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            end = time.time()
            sock.close()

            if result == 0:
                latency = round((end - start) * 1000, 2)
                latencies.append(latency)

            time.sleep(0.5) 

        except Exception:
            pass

    if latencies:
        avg = round(sum(latencies) / len(latencies), 2)
        min_l = min(latencies)
        max_l = max(latencies)
        logger.info(f"LATENCY     | {host:<20} | Avg: {avg}ms  Min: {min_l}ms  Max: {max_l}ms")
        return avg
    else:
        return None