#! /usr/bin/env python

from lib.ssdp import SSDPServer
import uuid
import netifaces as ni
from time import sleep
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_network_interface_ip_address(interface='wlan0')
    """
    Get the first IP address of a network interface.
    :param interface: The name of the interface.
    :return: The IP address.
    """
    while True:
        if NETWORK_INTERFACE not in ni.interfaces():
            logger.error('Could not find interface %s.' % (interface,))
            exit(1)
        interface = ni.ifaddresses(interface)
        if (2 not in interface) or (len(interface[2]) == 0):
            logger.warning('Could not find IP of interface %s. Sleeping.' % (interface,))
            sleep(60)
            continue
        return interface[2][0]['addr']


device_uuid = uuid.uuid4()

NETWORK_INTERFACE = 'wlan0'
local_ip_address = get_network_interface_ip_address(NETWORK_INTERFACE)

ssdp = SSDPServer()
ssdp.register('local',
              'uuid:{}::upnp:rootdevice'.format(device_uuid),
              'upnp:rootdevice',
              'http://{}:5000'.format(local_ip_address))
ssdp.run()
