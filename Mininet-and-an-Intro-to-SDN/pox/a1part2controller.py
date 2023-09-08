

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class Firewall(object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """

    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

        # add switch rules here
        self.install_firewall_rules()
        
    
    def install_firewall_rules(self):
    	"""
    	Install firewall rules to allow only ICMP and Arp traffic"
    	"""
    	
    	# Create a match object to allow only ICMP and ARP traffic
    	arp_match = of.ofp_match(dl_type=0x0806)  #ARP ehterype is 0x0806
    	
    	# Create a match object to match the ICMP packets
    	icmp_match = of.ofp_match(dl_type=0x0800, nw_proto=1)
    	
    	# Create a match object to match the IPv4 packets
    	ipv4_match = of.ofp_match(dl_type=0x0800)
    	
    	#Create actions to allow packets that match the rules
    	allow_action = of.ofp_action_output(port=of.OFPP_NORMAL)
    	
    	# Create actions to allow packets that match the rules
    	arp_rule = of.ofp_flow_mod()
    	arp_rule.match = arp_match
    	arp_rule.actions.append(allow_action)
    	
    	
    	# Create actions to allow packets that match the rules
    	icmp_rule = of.ofp_flow_mod()
    	icmp_rule.match = icmp_match
    	icmp_rule.actions.append(allow_action)
    	
    	# Create a rule to allow IPv4 traffic
    	ipv4_rule = of.ofp_flow_mod()
    	ipv4_rule.match = ipv4_match
    	ipv4_rule.actions.append(allow_action)
    	
    	
    	# send the connections to the switch
    	self.connection.send(arp_rule)
    	self.connection.send(icmp_rule)
    	self.connection.send(ipv4_rule)
    	
    	
    	#create a default drop rule for all the other traffic
    	default_drop_rule = of.ofp_flow_end()
    	default_drop_rule.priority = 0 # low priority so that other rules can work first
    	default_drop_rule.actions.append(of.ofp_action_output(port=of.OFPP_NONE)) # Drop the packet
    	self.connection.send(default_drop_rule)

    def _handle_PacketIn(self, event):
        """
        Packets not handled by the router rules will be
        forwarded to this method to be handled by the controller
        """

        packet = event.parsed  # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp  # The actual ofp_packet_in message.
        print("Unhandled packet :" + str(packet.dump()))


def launch():
    """
    Starts the component
    """
    
    def start_switch(event):
    	log.debug("Controlling %s" % (event.connection,))
    	Firewall(event.connection)
    	
    	
    core.openflow.addListenerByName("ConnectionUp",start_switch)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
