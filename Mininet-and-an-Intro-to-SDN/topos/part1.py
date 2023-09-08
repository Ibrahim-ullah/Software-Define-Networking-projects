#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI


class part1_topo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        self.addLink(h3,s1)
        self.addLink(h4,s1)



if __name__ == "__main__":
    t = part1_topo()
    net = Mininet(topo=t)
    net.start()
    
    # Get the host object ny name
    host1 = net.get('h1')
    host2 = net.get('h2')
    host3 = net.get('h3')
    host4 = net.get('h4')
    
    #set the ip address for the host
    
    host1.setIP('192.168.0.2/24')
    host2.setIP('192.168.0.3/24')
    host3.setIP('192.168.0.4/24')
    host4.setIP('192.168.0.5/24')
 
    
    
    CLI(net)
    net.stop()
