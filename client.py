import socket
import json

def query_server(graph, start):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))

    request = json.dumps({'graph': graph, 'start': start})
    client_socket.send(request.encode())

    response = client_socket.recv(4096)
    result = json.loads(response.decode())
    client_socket.close()

    return result

if __name__ == "__main__":
    graph = {
        'u': {'v': 7, 'w': 3, 'x': 5},
        'v': {'u': 7, 'w': 2},
        'w': {'u': 3, 'v': 2, 'x': 3, 'y': 8},
        'x': {'u': 5, 'w': 3, 'y': 4},
        'y': {'w': 8, 'x': 4, 'z': 2},
        'z': {'y': 2}
    }
    start = 'u'
    result = query_server(graph, start)

    print(f"최단 경로 비용: {result['distances']}")
    print(f"최단 경로: {result['paths']}")
    print(f"포워딩 테이블:")
    for dest, (src, next_hop) in result['forwarding_table'].items():
        print(f"{dest}: {src} -> {next_hop}")
