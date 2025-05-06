import heapq

def primsMST(graph, start):
    visited = set()
    mst = []
    minHeap = []

    visited.add(start)
    for neighbor, weight in graph[start]:
        heapq.heappush(minHeap, (weight, start, neighbor))

    while minHeap:
        weight, u, v = heapq.heappop(minHeap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, weight))
        for neighbor, w in graph[v]:
            if neighbor not in visited:
                heapq.heappush(minHeap, (w, v, neighbor))

    return mst


