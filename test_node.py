import node


test_node = node.Node()



going = True
x = ""
while going:
    test_node.handle_connections(verbose=True)
    test_node.handle_peers(verbose=True)
    x_str = input("~> ")
    x = ' '
    if len(x_str) > 0:
        x = x_str[0]
    x_list = x_str.split()
    if x == 'q':
        going = False
    elif x == 's':
        test_node.toggle_server(verbose=True)
    elif x == 'c':
        host = None
        if len(x_list) > 1:
            host = x_list[1]
        test_node.connect_to(host, verbose=True)
    elif x == 'd':
        host = None
        if len(x_list) > 1:
            host = x_list[1]
        test_node.disconnect_from(host, verbose=True)
    elif x == 'D':
        test_node.disconnect_all(verbose=True)
    elif x == 'b':
        test_node.broadcast_chat(x_str[len(x_list[0])+1:])
    elif x == 'p':
        test_node.n_peers(verbose=True)



test_node.stop_server(verbose=True)
test_node.disconnect_all(verbose=True)


