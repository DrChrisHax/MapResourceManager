import tkinter as tk
from tkinter import Canvas
import networkx as nx
import random

temp = "404: Value Not Found"  # Placeholder for resource values

class SimulationUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulation Home Page")
        self.root.geometry("1200x650")
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
        self.leftFrame = tk.Frame(self.mainFrame, width=800, height=600, bd=2, relief=tk.SUNKEN, bg="#33475b")
        self.leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))

        self.canvas = Canvas(self.leftFrame, width=800, height=600, bg="#33475b", highlightthickness=0)
        self.canvas.pack()

        self.graph = self.createRandomTree(numNodes=10)
        self.nodeWidgets = {}
        self.drawGraph()

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

    # --- Random Tree Graph Generation ---
    def createRandomTree(self, numNodes):
        tree = nx.Graph()
        nodes = list(range(numNodes))
        random.shuffle(nodes)
        for i in range(1, numNodes):
            u = nodes[i]
            v = random.choice(nodes[:i])
            tree.add_edge(u, v, weight=random.randint(1, 20))
        return tree

    def drawGraph(self):
        width = 800
        height = 600
        padding = 50
        positions = {}
        for node in self.graph.nodes():
            x = random.randint(padding, width - padding)
            y = random.randint(padding, height - padding)
            positions[node] = (x, y)
        self.positions = positions

        for u, v, data in self.graph.edges(data=True):
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="white")
            midX = (x1 + x2) / 2
            midY = (y1 + y2) / 2
            weight = data['weight']
            self.canvas.create_text(midX, midY, text=str(weight), fill="lightblue", font=("Arial", 10))

        nodeRadius = 15
        for node, (x, y) in positions.items():
            oval = self.canvas.create_oval(
                x - nodeRadius, y - nodeRadius, x + nodeRadius, y + nodeRadius,
                fill="#4da6ff", outline="white", tags=f"node_{node}"
            )
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 10), fill="white")

            self.nodeWidgets[node] = oval
            self.canvas.tag_bind(f"node_{node}", "<Enter>", lambda e, n=node: self.onNodeHover(n))
            self.canvas.tag_bind(f"node_{node}", "<Leave>", lambda e, n=node: self.onNodeLeave(n))

    def insertPlaceholderText(self):
        self.resourcesText.delete("1.0", tk.END)
        self.resourcesText.insert(tk.END, f"Police: {temp}\nFire: {temp}\nMedical: {temp}")

        self.incidentsText.delete("1.0", tk.END)
        self.incidentsText.insert(tk.END, "Please Enter Address,\nType of Incident,\nTime of Incident,\nPriority")

    def onNodeHover(self, node):
        oval = self.nodeWidgets.get(node)
        if oval:
            self.canvas.itemconfig(oval, fill="#66c2ff")

    def onNodeLeave(self, node):
        oval = self.nodeWidgets.get(node)
        if oval:
            self.canvas.itemconfig(oval, fill="#4da6ff")

    def startSimulation(self):
        print("Start button clicked! (Simulation not implemented yet)")

    def run(self):
        self.root.mainloop()
