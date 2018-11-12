from six.moves import input
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
from time import sleep
import logging
import socket
from typing import cast
IPaddr = "pp"

class MyListener (object):
    def remove_service(self, zeroconf, type, name):
        print("Service%sremoved" % (name,))
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        try:
            Name = info.name
        except:
            pass
        if(Name == "LED._http._tcp.local."):
            IPaddr = socket.inet_ntoa(cast(bytes, info.address))
            print(IPaddr)
            zeroconf.close()

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    print(IPaddr)
    zeroconf.close()


# def zeroconf_info():
#     """zeroconf_info returns a list of tuples of the information about other
#     zeroconf services on the local network. It does this by creating a
#     zeroconf.ServiceBrowser and spending 0.25 seconds querying the network for
#     other services."""
#     ret_info = []

#     def on_change(zeroconf, service_type, name, state_change):
#         if state_change is zeroconfig.ServiceStateChange.Added:
#             info = zeroconf.get_service_info(service_type, name)
#             if info:
#                 address = "{}".format(socket.inet_ntoa(info.address))
#                 props = str(info.properties.items())
#                 item = ServerInfo(str(info.server), address, info.port, props)
#                 ret_info.append(item)

#     zc = zeroconfig.Zeroconf()
#     browser = zeroconfig.ServiceBrowser(
#         zc, "_defusedivision._tcp.local.", handlers=[on_change])
#     sleep(1)
#     concurrency.concurrent(lambda: zc.close())()
#     return ret_info 

