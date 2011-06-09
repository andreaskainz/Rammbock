from Client import UDPClient, TCPClient
from Server import UDPServer, TCPServer
import Server
import Client
import Encode
import XmlParser
import imp
from os import getcwd


class Rammbock(object):

    def __init__(self):
        self.message = None
        self._servers = {}
        self._clients = {}

    def start_udp_server(self, nwinterface, port, ip=Server.DEFAULT_IP, name=Server.DEFAULT_NAME):
        self._servers[name] = UDPServer(name)
        self._servers[name].server_startup(nwinterface, ip, port)

    def start_tcp_server(self, nwinterface, port, ip=Server.DEFAULT_IP, name=Server.DEFAULT_NAME):
        self._servers[name] = TCPServer(name)
        self._servers[name].server_startup(nwinterface, ip, port)

    def check_server_status(self, name=Server.DEFAULT_NAME):
        return name in self._servers

    def check_client_status(self, name=Client.DEFAULT_NAME):
        return name in self._clients

    def connect_to_udp_server(self, host, port, ifname = False, client=Client.DEFAULT_NAME):
        self._clients[client].establish_connection_to_server(host, port, ifname)

    def connect_to_tcp_server(self, host, port, ifname = False, client=Client.DEFAULT_NAME):
        self._clients[client].establish_connection_to_server(host, port, ifname)

    def accept_tcp_connection(self, server=Server.DEFAULT_NAME):
        self._servers[server].accept_connection()

    def close_server(self, name=Server.DEFAULT_NAME):
        self._servers[name].close()
        del self._servers[name]

    def create_udp_client(self, name=Client.DEFAULT_NAME):
        self._clients[name] = UDPClient(name)

    def create_tcp_client(self, name=Client.DEFAULT_NAME):
        self._clients[name] = TCPClient(name)

    def close_client(self, name=Client.DEFAULT_NAME):
        self._clients[name].close()
        del self._clients[name] 

    def client_sends_data(self, packet, name=Client.DEFAULT_NAME): 
        self._clients[name].send_packet(packet)

    def server_receives_data(self, name=Server.DEFAULT_NAME):
        return self._servers[name].server_receives_data()

    def client_receives_data(self, name=Client.DEFAULT_NAME):
        return self._clients[name].receive_data()

    def server_sends_data(self, packet, name=Server.DEFAULT_NAME): 
        self._servers[name].send_data(packet)

    def client_sends_message(self, client_name=Client.DEFAULT_NAME, server_name=Server.DEFAULT_NAME):
        data_bin = Encode.encode_to_bin(self.message)
        self.client_sends_data(data_bin)

    def use_application_protocol(self, name, version=1):
        self.application_protocol = name
        self.version = version

    def create_message(self, name):
        msg = imp.load_source("Message", "src/rammbock/protocols/"+self.application_protocol+"/"+self.version+".py")
        self.message = msg.Message(name)

    def get_header_field(self, name):
        for hdr in self.message.header:
            if hdr.name == name:
                return hdr.data

    def get_information_element(self, name):
        fetchable = self.message
        for f_name in name.rsplit('.'):
            try:
                fetchable = (x for x in fetchable.ie if x.name == f_name).next()
            except StopIteration:
                raise Exception('Information element not found!')
        return fetchable.data

    def add_information_element(self, name, value=None):
        self._add_ie_to_node(self.message.ie, name.rsplit('.'), value) 

    def modify_information_element(self, name, value):
        self.add_information_element(name, value)

    def add_header_field(self, name, value):
        add = XmlParser.DataNode()
        add.name = name
        add.data = value
        if len(self.message.header) is 1:
            self.message.header = [self.message.header]
        self.message.header.append(add)

    def modify_header_field(self, name, value):
        try:
            a = ((i,x) for i,x in enumerate(self.message.header) if x.name == name).next()
            self.message.header[a[0]].data = value
        except StopIteration:
            self.add_header_field(name, value)

    def _add_ie_to_node(self, node, name, value):
        if name:
            try:
                fetchable = (x for x in node if x.name == name[0]).next()
            except StopIteration: #not found -> add
                add = XmlParser.DataNode()
                add.name = name[0]
                add.ie = []
                node.append(add)
                fetchable = add
            if len(name) is 1:
                fetchable.data = value
            self._add_ie_to_node(fetchable.ie, name[1:], value)

    def delete_information_element(self, name):
        splitted = name.rsplit('.')
        fetchable = self.message
        for f_name in splitted:
            a_fetchable = ((i,x) for i,x in enumerate(fetchable.ie) if x.name == f_name).next()
            if f_name is splitted[-1]:
                try:
                    del fetchable.ie[a_fetchable[0]]
                except AttributeError:
                    del fetchable.ie
            fetchable = a_fetchable[1]

    def delete_header_field(self, name):
        a = ((i,x) for i,x in enumerate(self.message.header) if x.name == name).next()
        try:
            del self.message.header[a[0]]
        except AttributeError:
            del self.message.header

