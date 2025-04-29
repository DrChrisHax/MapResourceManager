import heapq

def dijkstraPath(graphDict: dict[str, list[tuple[str, int]]], start: str, end: str):
    visited = set()
    minHeap = [(0, start, [])]  # (currentDistance, currentNode, pathList)

    while minHeap:
        cost, node, path = heapq.heappop(minHeap)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node == end:
            return path, cost

        for neighbor, weight in graphDict.get(node, []):
            if neighbor not in visited:
                heapq.heappush(minHeap, (cost + weight, neighbor, path))

    return None, float('inf')  # No path

