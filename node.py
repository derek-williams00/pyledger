import socket


PORT = 50505
SERVER_BACKLOG = 5
SERVER_TIMEOUT = 0.5
HEADER_SIZE = 256


class Node:
    def __init__(self):
        self.server_socket = None
        self.peer_sockets = dict()

    def start_server(self, verbose=False):
        if self.server_socket == None:
            if verbose:
                print("Starting server ...")
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.settimeout(SERVER_TIMEOUT)
                self.server_socket.bind(('', PORT))
                self.server_socket.listen(SERVER_BACKLOG)
            except OSError:
                if verbose:
                    print("Failed to start server.")
                self.server_socket = None
        elif verbose:
            print("Server already started.")

    def stop_server(self, verbose=False):
        if self.server_socket != None:
            if verbose:
                print("Stopping server ...")
            self.server_socket.close()
            self.server_socket = None

    def toggle_server(self, verbose=False):
        if self.server_socket == None:
            self.start_server(verbose=verbose)
        else:
            self.stop_server(verbose=verbose)

    def handle_connections(self, verbose=False):
        if self.server_socket != None:
            try:
                client_socket, client_addr = self.server_socket.accept()
                client_socket.setblocking(False)
                client_socket.settimeout(SERVER_TIMEOUT)
                self.peer_sockets[client_addr] = client_socket
                if verbose:
                    print("New connection {}".format(client_addr))
                    print("PEERS :", len(self.peer_sockets))
                return True
            except socket.timeout:
                return False

    def connect_to(self, host=None, verbose=False):
        if host == None:
            host = socket.gethostname()
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.settimeout(SERVER_TIMEOUT)
            new_socket.connect((host, PORT))
            self.peer_sockets[host] = new_socket
            if verbose:
                print("New connection {}".format(host))
                print("PEERS :", len(self.peer_sockets))
            return True
        except ConnectionRefusedError:
            return False

    def disconnect_from(self, host=None, verbose=False):
        if host == None:
            self.disconnect_all(host, verbose=verbose)
            return
        old_socket = self.peer_sockets.pop(host)
        old_socket.close()
        if verbose:
            print("Closing connection {}".format(host))
            print("PEERS :", len(self.peer_sockets))

    def disconnect_all(self, verbose=False):
        for addr, peer_socket in self.peer_sockets.items():
            peer_socket.close()
            if verbose:
                print("Closing connection {}".format(addr))
        self.peer_sockets = dict()

    def broadcast_chat(self, msg):
        #try:
        for addr, peer_socket in self.peer_sockets.items():
            header = bytes("CHAT {}".format(len(msg)).ljust(HEADER_SIZE), "utf-8")
            peer_socket.send(header)
            peer_socket.send(bytes(msg, "utf-8"))
        #except :

    def handle_chat(self, addr, peer_socket, msg_len):
        result = str(addr) + ' : "'
        result += str(peer_socket.recv(msg_len), "utf-8")
        result += '"\n'
        return result

    def n_peers(self, verbose=False):
        if verbose:
            print("PEERS :", len(self.peer_sockets))
        return len(self.peer_sockets)

    def handle_peers(self, verbose=False):
        active_str = ""
        n_active = 0
        if verbose:
            if len(self.peer_sockets) > 0:
                active_str += "ACTIVE ({}/{}): "
        report = ""
        purge_list = []
        for addr, peer_socket in self.peer_sockets.items():
            header = None
            try:
                header = peer_socket.recv(256)
            except ConnectionResetError:
                purge_list.append(addr)
                continue
            except socket.timeout:
                pass
            if header == None:
                if verbose:
                    active_str += "x "
                continue
            if verbose:
                active_str += "* "
                n_active += 1
            header_str = str(header, "utf-8")
            header_list = header_str.split()
            if len(header_list) < 1:
                continue
            if verbose:
                print("{} -> {}".format(str(addr), header_str))
            if header_list[0] == "CHAT":
                report += self.handle_chat(addr, peer_socket, int(header_list[1]))
        for addr in purge_list:
            self.disconnect_from(addr)
            if verbose:
                print("Purging {}".format(str(addr)))
        if verbose:
            if n_active > 0:
                print(active_str.format(n_active, len(self.peer_sockets)))
            print(report, end='')

    def __del__(self):
        self.stop_server()
        self.disconnect_all()



