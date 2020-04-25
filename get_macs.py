"""
Extremely simple script that needs to run as root. This just prints out all
MAC addresses as they are identified on the local network.
"""

from scapy.all import sniff, ARP


def arp_capture(pkt):
    print(pkt[ARP].hwsrc)


if __name__ == '__main__':
    print(sniff(prn=arp_capture, filter="arp", store=0, count=0))
