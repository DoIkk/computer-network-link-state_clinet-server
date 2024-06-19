import socket
import json
import heapq

def dijkstra(graph, start):
    queue = [(0, start, [])]
    seen = set()
    min_dist = {start: 0}
    paths = {start: []}
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in seen:
            continue
        seen.add(node)
        path = path + [node]
        paths[node] = path
        for next_node, weight in graph.get(node, {}).items():
            if next_node in seen:
                continue
            prev = min_dist.get(next_node, None)
            next_cost = cost + weight
            if prev is None or next_cost < prev:
                min_dist[next_node] = next_cost
                heapq.heappush(queue, (next_cost, next_node, path))

    return min_dist, paths

def create_forwarding_table(paths, start):
    forwarding_table = {}
    for dest, path in paths.items():
        if dest == start or not path:
            continue
        forwarding_table[dest] = (start, path[1])
    return forwarding_table

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(1)
    print("서버가 9999 포트에서 실행 중입니다.")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"클라이언트 연결됨: {addr}")

        data = client_socket.recv(4096)
        if not data:
            break

        request = json.loads(data.decode())
        graph = request['graph']
        start = request['start']

        min_dist, paths = dijkstra(graph, start)
        forwarding_table = create_forwarding_table(paths, start)
        response = json.dumps({'distances': min_dist, 'paths': paths, 'forwarding_table': forwarding_table})
        client_socket.send(response.encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()
