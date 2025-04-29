# models/node.py
class Node:
    def __init__(self, nodeId: str, x: int, y: int, nodeType: str):
        self.nodeId = nodeId
        self.x = x
        self.y = y
        self.nodeType = nodeType  # "Red" or "Blue"
