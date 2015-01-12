__author__ = 'lniu'

import re

# Add client according to hosts
def fetch_all_hosts(hosts_file):
    all_hosts = [];
    for line in open(hosts_file):
        if re.match('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}).*', line):
            line_split = line.split();
            all_hosts.append({'Hostname':line_split[1], 'ip': line_split[0]});
    return all_hosts

# return client xml element based on pass in host.
# host format: {'Hostname': value, 'ip' : value}
def get_client(host):
    return {'host': host['Hostname'], 'weight': '1', 'cpu': '2', 'maxusers': '40000'}

# print out a tree more human readable. But it add extract newline for each line.
# refer: http://stackoverflow.com/questions/17402323/use-xml-etree-elementtree-to-write-out-nicely-formatted-xml-files
from xml.dom import minidom
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

import sys
import xml.etree.ElementTree as ET

xml_file_path = sys.argv[1]
hosts_file_path = sys.argv[2]

hosts = fetch_all_hosts(hosts_file_path)
tree = ET.parse(xml_file_path)
root = tree.getroot()
clients = root.find('clients')
for host in hosts:
    ET.SubElement(clients, 'client', attrib=get_client(host))
tree.write(sys.stdout)




