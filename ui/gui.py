import tkinter as tk
from tkinter import Canvas
import networkx as nx
import random
import os

# For testing
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# End of Testing

from algorithms.dijkstra import dijkstraPath

from models.node import Node
from PIL import Image, ImageTk

temp = "404: Value Not Found"  # Placeholder for resource values

class SimulationUI:
    def __init__(self, engine):
        self.engine = engine
        self.root = tk.Tk()
        self.root.title("Simulation Home Page")
        self.root.geometry("1200x960")
        self.root.configure(bg="#2b3e50")
        self.root.overrideredirect(True)  # <-- Borderless window

        # ---------------- Custom Drag Bar ----------------
        self.titleBar = tk.Frame(self.root, bg="#1f2d3a", relief='raised', bd=0, height=40)
        self.titleBar.pack(fill=tk.X)

        self.titleLabel = tk.Label(self.titleBar, text="Simulation Home Page", bg="#1f2d3a", fg="white", font=("Helvetica", 14))
        self.titleLabel.pack(side=tk.LEFT, padx=10)

        self.closeButton = tk.Button(self.titleBar, text="X", command=self.root.quit,
                                     bg="#ff6666", fg="white", bd=0, font=("Helvetica", 12, "bold"),
                                     activebackground="#cc5555", activeforeground="white",
                                     width=3, height=1, relief="flat", highlightthickness=0)
        self.closeButton.configure(
            padx=7, pady=4, borderwidth=0, highlightbackground="#1f2d3a", highlightcolor="#1f2d3a"
        )
        self.closeButton.pack(side=tk.RIGHT, padx=10, pady=5)

        self.titleBar.bind("<ButtonPress-1>", self.startMove)
        self.titleBar.bind("<ButtonRelease-1>", self.stopMove)
        self.titleBar.bind("<B1-Motion>", self.onMove)

        # ---------------- Main Frame ----------------
        self.mainFrame = tk.Frame(self.root, bg="#2b3e50")
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # ---------------- Left side: Map and nodes ----------------
        self.leftFrame = tk.Frame(self.mainFrame, width=800, height=800, bd=2, relief=tk.SUNKEN, bg="#33475b")
        self.leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))

        self.canvas = Canvas(self.leftFrame, width=800, height=800, bg="#33475b", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.loadBackground()

        self.createCityMap()
        self.nodeWidgets = {}
        self.drawGraph()

        self.enableCoordinateClickHelper()

        # ---------------- Right side: Stack ----------------
        self.rightFrame = tk.Frame(self.mainFrame, width=400, height=600, padx=10, bg="#2b3e50")
        self.rightFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.incidentsLabel = tk.Label(self.rightFrame, text="Incidents", font=("Helvetica", 18),
                                       bg="#2b3e50", fg="white")
        self.incidentsLabel.pack(pady=(20, 5))

        self.incidentsText = tk.Text(self.rightFrame, height=8, width=40, bg="#3f5870",
                                     fg="white", insertbackground="white", relief=tk.GROOVE, bd=2)
        self.incidentsText.pack(pady=(0, 20))

        self.resourcesLabel = tk.Label(self.rightFrame, text="Resources", font=("Helvetica", 18),
                                       bg="#2b3e50", fg="white")
        self.resourcesLabel.pack(pady=(20, 5))

        self.resourcesText = tk.Text(self.rightFrame, height=8, width=40, bg="#3f5870",
                                     fg="white", insertbackground="white", relief=tk.GROOVE, bd=2)
        self.resourcesText.pack(pady=(0, 20))

        self.insertPlaceholderText()

        # ---------------- Bottom Buttons ----------------
        self.buttonFrame = tk.Frame(self.root, bg="#2b3e50")
        self.buttonFrame.pack(pady=10)

        self.startButton = tk.Button(self.buttonFrame, text="Start Simulation", command=self.startSimulation,
                                     bg="#4da6ff", fg="white", font=("Helvetica", 12, "bold"), width=20,
                                     activebackground="#3399ff", activeforeground="white")
        self.startButton.grid(row=0, column=0, padx=10)

        self.quitButton = tk.Button(self.buttonFrame, text="Quit", command=self.root.quit,
                                    bg="#ff6666", fg="white", font=("Helvetica", 12, "bold"), width=20,
                                    activebackground="#cc5555", activeforeground="white")
        self.quitButton.grid(row=0, column=1, padx=10)

        # --- Clock and Step Button ---
        self.clockTime = 0  # in minutes

        # Container to help center clock and step button together
        self.clockFrame = tk.Frame(self.titleBar, bg="#1f2d3a")
        self.clockFrame.pack(side=tk.TOP, pady=0, expand=True)

        self.clockLabel = tk.Label(self.clockFrame, text="Time: 00:00", bg="#1f2d3a", fg="white", font=("Helvetica", 12))
        self.clockLabel.pack(side=tk.LEFT, padx=5)

        # Testing purposes: increment clock by 1 minute
        self.stepButton = tk.Button(self.clockFrame, text="⏱️ +1 min", command=self.incrementClock,
                                    bg="#4da6ff", fg="white", font=("Helvetica", 10), bd=0,
                                    activebackground="#3399ff", activeforeground="white")
        self.stepButton.pack(side=tk.LEFT, padx=5)
        # End of Testing


    def incrementClock(self):
        self.clockTime = (self.clockTime + 1) % 1440  # Wraps after 1440 mins (24h) <-- This is where it increments
        hours, minutes = divmod(self.clockTime, 60)
        self.clockLabel.config(text=f"Time: {hours:02d}:{minutes:02d}")

    def enableCoordinateClickHelper(self):
        def onCanvasClick(event):
            x, y = event.x, event.y
            print(f"Clicked at: ({x}, {y})")
        
        self.canvas.bind("<Button-1>", onCanvasClick)   

    # --- Dragging functions for the title bar ---
    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def onMove(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def loadBackground(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))  # path to gui.py
        path = os.path.join(baseDir, '..', 'assets', 'map.PNG')
        path = os.path.normpath(path)

        print("Trying to open:", path)  # Debugging

        self.backgroundImage = Image.open(path)
        self.backgroundImage = self.backgroundImage.resize((800, 850))
        self.backgroundTk = ImageTk.PhotoImage(self.backgroundImage)



    def createCityMap(self):
        self.graph = nx.Graph()

        # ----------- Node positions (x, y) are adjustable here -----------
        # Feel free to tweak these values to match your map exactly
        self.nodes = [
            Node("Node 1 Red", 87, 121, "Red"),
            Node("Node 2 Red", 650, 121, "Red"),
            Node("Node 3 Red", 290, 229, "Red"),
            Node("Node 4 Red", 531, 335, "Red"),
            Node("Node 5 Red", 87, 437, "Red"),
            Node("Node 6 Red", 650, 437, "Red"),
            Node("Node 7 Red", 290, 540, "Red"),
            Node("Node 8 Red", 531, 645, "Red"),
            Node("Node 9 Red", 85, 746, "Red"),
            Node("Node 10 Red", 649, 748, "Red"),
            Node("Node 11 Blue", 291, 121, "Blue"),
            Node("Node 12 Blue", 530, 121, "Blue"),
            Node("Node 13 Blue", 88, 229, "Blue"),
            Node("Node 14 Blue", 531, 228, "Blue"),
            Node("Node 15 Blue", 650, 229, "Blue"),
            Node("Node 16 Blue", 87, 339, "Blue"),
            Node("Node 17 Blue", 290, 335, "Blue"),
            Node("Node 18 Blue", 650, 335, "Blue"),
            Node("Node 19 Blue", 291, 439, "Blue"),
            Node("Node 20 Blue", 531, 438, "Blue"),
            Node("Node 21 Blue", 88, 540, "Blue"),
            Node("Node 22 Blue", 531, 543, "Blue"),
            Node("Node 23 Blue", 649, 542, "Blue"),
            Node("Node 24 Blue", 84, 643, "Blue"), 
            Node("Node 25 Blue", 291, 643, "Blue"),
            Node("Node 26 Blue", 649, 646, "Blue"),
            Node("Node 27 Blue", 291, 748, "Blue"),
            Node("Node 28 Blue", 531, 747, "Blue"),
        ]

        # Add nodes to the graph
        for node in self.nodes:
            self.graph.add_node(node.nodeId, obj=node)

        # ----------- Edges and Weights -----------
        edges = [
            ("Node 1 Red", "Node 11 Blue", 41),
            ("Node 11 Blue", "Node 12 Blue", 48),
            ("Node 12 Blue", "Node 2 Red", 24),

            ("Node 1 Red", "Node 13 Blue", 22),
            ("Node 13 Blue", "Node 3 Red", 41),
            ("Node 3 Red", "Node 14 Blue", 48),
            ("Node 14 Blue", "Node 15 Blue", 24),
            ("Node 15 Blue", "Node 2 Red", 42),

            ("Node 13 Blue", "Node 16 Blue", 22),
            ("Node 16 Blue", "Node 5 Red", 20),
            ("Node 3 Red", "Node 17 Blue", 21),
            ("Node 17 Blue", "Node 4 Red", 48),
            ("Node 4 Red", "Node 18 Blue", 24),
            ("Node 18 Blue", "Node 15 Blue", 21),

            ("Node 5 Red", "Node 21 Blue", 20),
            ("Node 21 Blue", "Node 7 Red", 41),
            ("Node 7 Red", "Node 19 Blue", 21),
            ("Node 19 Blue", "Node 20 Blue", 48),
            ("Node 20 Blue", "Node 6 Red", 24),

            ("Node 5 Red", "Node 24 Blue", 21),
            ("Node 24 Blue", "Node 25 Blue", 41),
            ("Node 25 Blue", "Node 8 Red", 48),
            ("Node 8 Red", "Node 22 Blue", 21),
            ("Node 22 Blue", "Node 23 Blue", 24),
            ("Node 23 Blue", "Node 6 Red", 21),

            ("Node 9 Red", "Node 27 Blue", 41),
            ("Node 27 Blue", "Node 28 Blue", 48),
            ("Node 28 Blue", "Node 10 Red", 24),

            # Your requested extra vertical edges
            ("Node 11 Blue", "Node 3 Red", 21),
            ("Node 12 Blue", "Node 14 Blue", 21),
            ("Node 14 Blue", "Node 4 Red", 21),
            ("Node 16 Blue", "Node 17 Blue", 41),
            ("Node 5 Red", "Node 19 Blue", 41),
            ("Node 17 Blue", "Node 19 Blue", 21),
            ("Node 4 Red", "Node 20 Blue", 21),
            ("Node 18 Blue", "Node 6 Red", 21),
            ("Node 7 Red", "Node 22 Blue", 48),
            ("Node 7 Red", "Node 25 Blue", 21),
            ("Node 23 Blue", "Node 26 Blue", 21),
            ("Node 24 Blue", "Node 9 Red", 21),
            ("Node 25 Blue", "Node 27 Blue", 21),
            ("Node 8 Red", "Node 28 Blue", 20),
            ("Node 8 Red", "Node 26 Blue", 24),
            ("Node 26 Blue", "Node 10 Red", 21),
            ("Node 20 Blue", "Node 22 Blue", 21)
        ]



        for u, v, weight in edges:
            self.graph.add_edge(u, v, weight=weight)


    def drawGraph(self):
        self.canvas.delete("all")  # Clear previous drawings if any

        # Draw Map
        self.canvas.create_image(0, 0, image=self.backgroundTk, anchor="nw")

        # Draw edges (commented out for now, will uncomment after testing)
        # for u, v, data in self.graph.edges(data=True):
        #     nodeU = self.graph.nodes[u]['obj']
        #     nodeV = self.graph.nodes[v]['obj']
        #     x1, y1 = nodeU.x, nodeU.y
        #     x2, y2 = nodeV.x, nodeV.y

        #     self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)
        #     midX = (x1 + x2) / 2
        #     midY = (y1 + y2) / 2
        #     weight = data['weight']
        #     self.canvas.create_text(midX, midY, text=str(weight), fill="darkblue", font=("Arial", 10))

        # Draw edges (to make edges more clear, comment out after testing)
        for u, v, data in self.graph.edges(data=True):
            nodeU = self.graph.nodes[u]['obj']
            nodeV = self.graph.nodes[v]['obj']
            x1, y1 = nodeU.x, nodeU.y
            x2, y2 = nodeV.x, nodeV.y

            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

            midX = (x1 + x2) / 2
            midY = (y1 + y2) / 2
            weight = data['weight']

            # --- Add background box for better readability ---
            textPadding = 4
            textFont = ("Arial", 10)
            textId = self.canvas.create_text(midX, midY, text=str(weight), font=textFont)

            bbox = self.canvas.bbox(textId)  # (x1, y1, x2, y2) of text
            if bbox:
                x1_box, y1_box, x2_box, y2_box = bbox
                rectId = self.canvas.create_rectangle(
                    x1_box - textPadding, y1_box - textPadding,
                    x2_box + textPadding, y2_box + textPadding,
                    fill="white", outline=""
                )
                # Raise text above rectangle
                self.canvas.tag_raise(textId, rectId)


        # Draw nodes
        nodeRadius = 15
        self.nodeWidgets = {}
        for node in self.nodes:
            fillColor = "#ff4d4d" if node.nodeType == "Red" else "#4da6ff"  # Red or Blue
            oval = self.canvas.create_oval(
                node.x - nodeRadius, node.y - nodeRadius,
                node.x + nodeRadius, node.y + nodeRadius,
                fill=fillColor, outline="white", tags=f"node_{node.nodeId}"
            )
            self.canvas.create_text(node.x, node.y, text=node.nodeId.split()[1], font=("Arial", 8), fill="white")

            self.nodeWidgets[node.nodeId] = oval
            self.canvas.tag_bind(f"node_{node.nodeId}", "<Enter>", lambda e, n=node: self.onNodeHover(n.nodeId))
            self.canvas.tag_bind(f"node_{node.nodeId}", "<Leave>", lambda e, n=node: self.onNodeLeave(n.nodeId))

    def insertPlaceholderText(self):
        self.resourcesText.delete("1.0", tk.END)
        self.resourcesText.insert(tk.END, f"Police: {temp}\nFire: {temp}\nMedical: {temp}")

        self.incidentsText.delete("1.0", tk.END)
        self.incidentsText.insert(tk.END, "Please Enter Address,\nType of Incident,\nTime of Incident,\nPriority")

    def updateDashboard(self, policeCount: int, fireCount: int, medicalCount: int,
                    address: str, incidentType: str, time: str, priority: str):
        """
        Update the resources and incidents text boxes with provided values.
        Can be called by the engine.
        """
        self.resourcesText.delete("1.0", tk.END)
        self.resourcesText.insert(
            tk.END,
            f"Police: {policeCount}\nFire: {fireCount}\nMedical: {medicalCount}"
        )

        self.incidentsText.delete("1.0", tk.END)
        self.incidentsText.insert(
            tk.END,
            f"Address: {address}\nType: {incidentType}\nTime: {time}\nPriority: {priority}"
        )

    # Testing Purposes
    def testUpdateDashboard(self):
        self.updateDashboard(
            policeCount=3,
            fireCount=2,
            medicalCount=1,
            address="123 Elm Street",
            incidentType="Fire",
            time="14:30",
            priority="High"
    )
    # End of Testing


    def onNodeHover(self, node):
        oval = self.nodeWidgets.get(node)
        if oval:
            self.canvas.itemconfig(oval, fill="#66c2ff")

    def onNodeLeave(self, node):
        oval = self.nodeWidgets.get(node)
        if oval:
            self.canvas.itemconfig(oval, fill="#4da6ff")

    def graphToDict(self):
        adj = {}
        for u, v, data in self.graph.edges(data=True):
            adj.setdefault(u, []).append((v, data["weight"]))
            adj.setdefault(v, []).append((u, data["weight"]))  # Because it's undirected
        return adj


    def animatePath(self, path: list[str], resourceType: int = 0):
        if not path:
            print("No path to animate.")
            return

        # Map resource types to sprite file paths
        spritePathMap = {
            1: "../assets/ambulance.png",
            2: "../assets/police.png",
            3: "../assets/firetruck.png",
            0: "../assets/generic.png"
        }

        spritePath = spritePathMap.get(resourceType, "../assets/generic.png")

        try:
            image = Image.open(os.path.join(os.path.dirname(__file__), spritePath))
            image = image.resize((30, 30), Image.Resampling.LANCZOS)  # Use .Resampling.LANCZOS for Pillow >=10
            spriteImg = ImageTk.PhotoImage(image)
        except Exception as e:
            print("Error loading sprite image:", e)
            return

        # Store image reference to prevent garbage collection
        self.spriteImg = spriteImg

        # Place the sprite at the start node
        startNode = self.graph.nodes[path[0]]['obj']
        sprite = self.canvas.create_image(startNode.x, startNode.y, image=spriteImg)

        # Move the sprite along the path
        for i in range(len(path) - 1):
            fromNode = self.graph.nodes[path[i]]['obj']
            toNode = self.graph.nodes[path[i + 1]]['obj']
            self.moveSprite(sprite, fromNode.x, fromNode.y, toNode.x, toNode.y)

        self.canvas.delete(sprite)  # optional: remove sprite at end

    


    def moveSprite(self, spriteId, x1, y1, x2, y2):
        steps = 20
        delay = 25  # ms per step
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        for _ in range(steps):
            self.canvas.move(spriteId, dx, dy)
            self.canvas.update()
            self.canvas.after(delay)

    def testDispatch(self):
        graphDict = self.graphToDict()
        path, total = dijkstraPath(graphDict, "Node 1 Red", "Node 10 Red")
        print("Path found:", path)
        print("Total travel time:", total)
        self.animatePath(path, resourceType=2)  # 2 = Police



    def startSimulation(self):
        print("Start button clicked!")
        self.engine.Start()
        # Testing Purposes
        self.testDispatch()
        self.testUpdateDashboard()  
        # End of Testing

    def run(self):
        self.root.mainloop()

# Testing Purposes
if __name__ == "__main__":
    class MockEngine:
        def Start(self):
            print("MockEngine.Start() called")

    ui = SimulationUI(MockEngine())
    ui.run()
# End of Testing