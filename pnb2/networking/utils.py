"""
"""
import ipaddress
import urllib.request
import socket


def find_external_address():
    """
    """
    try:
        address = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        ipaddress.ip_address(address)
    except Exception:
        raise Exception('Could not find external address')
    return address


def find_internal_address():
    """
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            address = s.getsockname()[0]
        ipaddress.ip_address(address)
    except Exception:
        raise Exception('Could not find internal address')
    return address

