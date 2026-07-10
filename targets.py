"""targets.py
List of devices to monitor.
Update this file to add or remove devices.
"""

TARGETS = [
    {
        'name':  'Google DNS',
        'host':  '8.8.8.8',
        'ports': [53, 443],       # DNS and HTTPS ports
    },
    {
        'name':  'Cloudflare DNS',
        'host':  '1.1.1.1',
        'ports': [53, 443],       # DNS and HTTPS ports
    },
    {
        'name':  'Google Web',
        'host':  '142.250.192.46',
        'ports': [80, 443],       # HTTP and HTTPS ports
    },
]

# common port numbers for reference
COMMON_PORTS = {
    22:  'SSH',
    23:  'Telnet',
    25:  'SMTP',
    53:  'DNS',
    80:  'HTTP',
    443: 'HTTPS',
    830: 'NETCONF',
}