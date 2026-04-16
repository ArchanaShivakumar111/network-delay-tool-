from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, icmp
from pox.lib.addresses import IPAddr
import time

log = core.getLogger()

# Blocked pair: h1 <-> h3
BLOCKED = [('10.0.0.1', '10.0.0.3'), ('10.0.0.3', '10.0.0.1')]

class DelayController(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_table = {}
        self.ping_times = {}
        connection.addListeners(self)
        log.info("Controller connected to switch: %s" % dpidToStr(connection.dpid))

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        in_port = event.port
        src_mac = str(packet.src)
        dst_mac = str(packet.dst)

        # MAC learning
        self.mac_table[src_mac] = in_port

        # Check IP layer
        ip_packet = packet.find('ipv4')
        if ip_packet:
            src_ip = str(ip_packet.srcip)
            dst_ip = str(ip_packet.dstip)

            # Firewall: block h1 <-> h3
            if (src_ip, dst_ip) in BLOCKED:
                log.info("BLOCKED: %s -> %s" % (src_ip, dst_ip))
                msg = of.ofp_flow_mod()
                msg.priority = 100
                msg.match.dl_type = 0x0800
                msg.match.nw_src = IPAddr(src_ip)
                msg.match.nw_dst = IPAddr(dst_ip)
                # No actions = drop
                self.connection.send(msg)
                return

            # ICMP RTT measurement
            icmp_packet = packet.find('icmp')
            if icmp_packet:
                if icmp_packet.type == 8:  # Echo request
                    key = (src_ip, dst_ip, icmp_packet.seq)
                    self.ping_times[key] = time.time()
                    log.info("ICMP Request: %s -> %s seq=%d" % (src_ip, dst_ip, icmp_packet.seq))
                elif icmp_packet.type == 0:  # Echo reply
                    key = (dst_ip, src_ip, icmp_packet.seq)
                    if key in self.ping_times:
                        rtt = (time.time() - self.ping_times[key]) * 1000
                        log.info("RTT: %s -> %s = %.3f ms" % (dst_ip, src_ip, rtt))
                        del self.ping_times[key]

        # Forward packet
        if dst_mac in self.mac_table:
            out_port = self.mac_table[dst_mac]
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, in_port)
            msg.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg)
        else:
            # Flood
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)

def launch():
    def start_switch(event):
        DelayController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
