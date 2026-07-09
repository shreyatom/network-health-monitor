# health_check.py
# Checks device connectivity, latency, and port availability
# using Python's built-in socket library.
# No external libraries needed — pure Python!

import socket
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import logger

# ── Function 1: Ping using socket ─────────────────────────────────────────
def check_connectivity(host, timeout=3):
    """
    Checks if a host is reachable by attempting a TCP connection.
    Returns: (is_reachable, latency_ms)
    """
    try:
        start_time = time.time()

        # Create a socket object
        # AF_INET = IPv4, SOCK_STREAM = TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Try connecting to port 80 (HTTP)
        # If device responds, it is reachable
        result = sock.connect_ex((host, 80))
        sock.close()

        end_time = time.time()

        # Calculate latency in milliseconds
        latency_ms = round((end_time - start_time) * 1000, 2)

        if result == 0:
            logger.info(f"REACHABLE   | {host:<20} | Latency: {latency_ms} ms")
            return True, latency_ms
        else:
            # Try port 443 if 80 failed
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


# ── Function 2: Check TCP port availability ────────────────────────────────
def check_port(host, port, timeout=3):
    """
    Checks if a specific TCP port is open on a host.
    Returns: True if port is open, False if closed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # connect_ex returns 0 if connection succeeded (port open)
        # returns non-zero if connection failed (port closed)
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


# ── Function 3: Get latency multiple times ─────────────────────────────────
def measure_latency(host, port=443, attempts=3):
    """
    Measures latency multiple times and returns average.
    More accurate than single measurement.
    Returns: average latency in ms or None if unreachable
    """
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

            time.sleep(0.5)  # small gap between attempts

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