from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from collections import deque
import heapq

@dataclass
class Building:
    id: int; name: str; location: str
    connections: List[Tuple[int,float]] = field(default_factory=list)
    def __str__(self)->str: return f"({self.id}) {self.name} - {self.location}"

class BSTNode:
    def __init__(self,b:Building): self.b=b; self.left=None; self.right=None

class BST:
    def __init__(self): self.root:Optional[BSTNode]=None
    def insertBuilding(self,b:Building):
        def _ins(n:Optional[BSTNode])->BSTNode:
            if n is None: return BSTNode(b)
            if b.id < n.b.id: n.left=_ins(n.left)
            elif b.id > n.b.id: n.right=_ins(n.right)
            else: n.b=b
            return n
        self.root=_ins(self.root)
    def search(self,key:int)->Optional[Building]:
        cur=self.root
        while cur:
            if key==cur.b.id: return cur.b
            cur = cur.left if key < cur.b.id else cur.right
        return None
    def inorder(self)->List[Building]:
        out:List[Building]=[]
        def _in(n:Optional[BSTNode]):
            if not n: return
            _in(n.left); out.append(n.b); _in(n.right)
        _in(self.root); return out
    def preorder(self)->List[Building]:
        out:List[Building]=[]
        def _pre(n:Optional[BSTNode]):
            if not n: return
            out.append(n.b); _pre(n.left); _pre(n.right)
        _pre(self.root); return out
    def postorder(self)->List[Building]:
        out:List[Building]=[]
        def _post(n:Optional[BSTNode]):
            if not n: return
            _post(n.left); _post(n.right); out.append(n.b)
        _post(self.root); return out
    def height(self)->int:
        def _h(n:Optional[BSTNode])->int:
            if not n: return 0
            return 1+max(_h(n.left),_h(n.right))
        return _h(self.root)

class AVLNode:
    def __init__(self,b:Building): self.b=b; self.left=None; self.right=None; self.h=1

class AVL:
    def __init__(self): self.root:Optional[AVLNode]=None
    def _height(self,n:Optional[AVLNode])->int: return n.h if n else 0
    def _update(self,n:AVLNode): n.h = 1 + max(self._height(n.left), self._height(n.right))
    def _bf(self,n:Optional[AVLNode])->int:
        if not n: return 0
        return self._height(n.left)-self._height(n.right)
    def _rot_right(self,y:AVLNode)->AVLNode:
        x=y.left; T2=x.right; x.right=y; y.left=T2
        self._update(y); self._update(x); return x
    def _rot_left(self,x:AVLNode)->AVLNode:
        y=x.right; T2=y.left; y.left=x; x.right=T2
        self._update(x); self._update(y); return y
    def insertBuilding(self,b:Building):
        def _ins(node:Optional[AVLNode])->AVLNode:
            if node is None: return AVLNode(b)
            if b.id < node.b.id: node.left=_ins(node.left)
            elif b.id > node.b.id: node.right=_ins(node.right)
            else: node.b=b; return node
            self._update(node); bal=self._bf(node)
            if bal>1 and b.id < node.left.b.id:
                print(f"AVL rotation LL at {node.b.id}"); return self._rot_right(node)
            if bal<-1 and b.id > node.right.b.id:
                print(f"AVL rotation RR at {node.b.id}"); return self._rot_left(node)
            if bal>1 and b.id > node.left.b.id:
                print(f"AVL rotation LR at {node.b.id}"); node.left=self._rot_left(node.left); return self._rot_right(node)
            if bal<-1 and b.id < node.right.b.id:
                print(f"AVL rotation RL at {node.b.id}"); node.right=self._rot_right(node.right); return self._rot_left(node)
            return node
        self.root=_ins(self.root)
    def inorder(self)->List[Building]:
        out:List[Building]=[]
        def _in(n:Optional[AVLNode]):
            if not n: return
            _in(n.left); out.append(n.b); _in(n.right)
        _in(self.root); return out
    def height(self)->int: return self._height(self.root)

class ExprNode:
    def __init__(self,val:str): self.val=val; self.left=None; self.right=None
def build_expression_tree(postfix:List[str])->Optional[ExprNode]:
    ops={'+','-','*','/','^'}; stack:List[ExprNode]=[]
    for tok in postfix:
        if tok in ops:
            if len(stack)<2: raise ValueError("Invalid postfix")
            r=stack.pop(); l=stack.pop()
            n=ExprNode(tok); n.left=l; n.right=r; stack.append(n)
        else: stack.append(ExprNode(tok))
    return stack[0] if stack else None
def evaluate_expression(node:Optional[ExprNode], vars:Optional[Dict[str,float]]=None)->float:
    if vars is None: vars={}
    if node is None: return 0.0
    if node.val not in ['+','-','*','/','^']:
        try: return float(node.val)
        except Exception:
            if node.val in vars: return float(vars[node.val])
            raise KeyError(f"Undefined variable '{node.val}'")
    L=evaluate_expression(node.left,vars); R=evaluate_expression(node.right,vars)
    if node.val=='+': return L+R
    if node.val=='-': return L-R
    if node.val=='*': return L*R
    if node.val=='/':
        if R==0: raise ZeroDivisionError("Division by zero")
        return L/R
    if node.val=='^': return L**R
    raise ValueError("Unknown operator")

class Graph:
    def __init__(self,n:int):
        self.n=n
        self.adj:Dict[int,List[Tuple[int,float]]] = {i:[] for i in range(1,n+1)}
        self.mat:List[List[Optional[float]]] = [[None]*(n+1) for _ in range(n+1)]
    def add_edge(self,u:int,v:int,w:float,undirected:bool=True):
        self.adj[u].append((v,w)); self.mat[u][v]=w
        if undirected:
            self.adj[v].append((u,w)); self.mat[v][u]=w
    def bfs(self,s:int)->List[int]:
        visited=set([s]); q=deque([s]); order:List[int]=[]
        while q:
            u=q.popleft(); order.append(u)
            for v,_ in self.adj[u]:
                if v not in visited: visited.add(v); q.append(v)
        return order
    def dfs(self,s:int)->List[int]:
        visited=set(); order:List[int]=[]
        def _d(u:int):
            visited.add(u); order.append(u)
            for v,_ in self.adj[u]:
                if v not in visited: _d(v)
        _d(s); return order
    def dijkstra(self,src:int):
        dist={i:float('inf') for i in range(1,self.n+1)}
        prev={i:None for i in range(1,self.n+1)}
        dist[src]=0; pq=[(0,src)]
        while pq:
            d,u=heapq.heappop(pq)
            if d>dist[u]: continue
            for v,w in self.adj[u]:
                nd=d+w
                if nd<dist[v]:
                    dist[v]=nd; prev[v]=u; heapq.heappush(pq,(nd,v))
        return dist,prev
    def kruskal(self):
        edges:List[Tuple[float,int,int]]=[]; seen=set()
        for u in self.adj:
            for v,w in self.adj[u]:
                if (v,u) not in seen:
                    edges.append((w,u,v)); seen.add((u,v))
        edges.sort()
        parent={i:i for i in range(1,self.n+1)}; rank={i:0 for i in range(1,self.n+1)}
        def find(x:int)->int:
            while parent[x]!=x:
                parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def union(a:int,b:int)->bool:
            ra,rb=find(a),find(b)
            if ra==rb: return False
            if rank[ra]<rank[rb]: parent[ra]=rb
            elif rank[ra]>rank[rb]: parent[rb]=ra
            else: parent[rb]=ra; rank[ra]+=1
            return True
        mst:List[Tuple[int,int,float]]=[]
        for w,u,v in edges:
            if union(u,v): mst.append((u,v,w))
        return mst

class CampusPlanner:
    def __init__(self):
        self.buildings:Dict[int,Building]={}
        self.bst=BST(); self.avl=AVL(); self.graph:Optional[Graph]=None
    def addBuildingRecord(self,b:Building):
        self.buildings[b.id]=b; self.bst.insertBuilding(b); self.avl.insertBuilding(b)
    def listCampusLocations(self)->Tuple[int,int]:
        print("BST Inorder:", [str(x) for x in self.bst.inorder()])
        print("BST Preorder:", [str(x) for x in self.bst.preorder()])
        print("BST Postorder:", [str(x) for x in self.bst.postorder()])
        print("AVL Inorder:", [str(x) for x in self.avl.inorder()])
        h_bst=self.bst.height(); h_avl=self.avl.height()
        print(f"Height -> BST: {h_bst}, AVL: {h_avl}")
        return h_bst,h_avl
    def constructCampusGraph(self,edges:List[Tuple[int,int,float]],undirected:bool=True):
        if not self.buildings: raise ValueError("No buildings added")
        n=max(self.buildings.keys()); self.graph=Graph(n)
        for u,v,w in edges:
            self.graph.add_edge(u,v,w,undirected=undirected)
            self.buildings[u].connections.append((v,w))
            if undirected: self.buildings[v].connections.append((u,w))
        print("Adjacency List:")
        for i in sorted(self.graph.adj.keys()): print(i,"->",self.graph.adj[i])
        print("Adjacency Matrix (non-None):")
        for i in range(1,self.graph.n+1):
            row=[(j,self.graph.mat[i][j]) for j in range(1,self.graph.n+1) if self.graph.mat[i][j] is not None]
            print(i,"->",row)
    def findOptimalPath(self,source:int,dest:int):
        if not self.graph: raise ValueError("Graph not constructed")
        dist,prev=self.graph.dijkstra(source)
        if dist[dest]==float('inf'): print("No path"); return None,None
        path=[]; cur=dest
        while cur is not None:
            path.append(cur); cur=prev[cur]
        path.reverse()
        print(f"Shortest path {source}->{dest}: distance={dist[dest]}, path={path}")
        return dist[dest],path
    def planUtilityLayout(self):
        if not self.graph: raise ValueError("Graph not constructed")
        mst=self.graph.kruskal(); print("Kruskal MST edges:",mst); return mst
    def evaluateExpression(self,postfix:List[str],vars:Optional[Dict[str,float]]=None):
        root=build_expression_tree(postfix); val=evaluate_expression(root,vars); print("Expression result:",val); return val

if __name__=="__main__":
    planner=CampusPlanner()
    sample_buildings=[
        Building(4,"Admin","Central"),
        Building(2,"Library","North"),
        Building(6,"CSE","Block A"),
        Building(1,"Cafe","South"),
        Building(3,"Lab","Block C"),
        Building(5,"Auditorium","East"),
    ]
    for b in sample_buildings: planner.addBuildingRecord(b)
    print("\n--- Tree Traversals & Height Comparison ---")
    planner.listCampusLocations()
    print("\n--- Construct Campus Graph ---")
    edges=[
        (1,2,50),(1,3,30),(2,3,20),
        (2,4,60),(3,4,15),(3,5,40),
        (4,6,70),(5,6,10)
    ]
    planner.constructCampusGraph(edges,undirected=True)
    print("\n--- Graph Traversals (BFS & DFS) ---")
    if planner.graph:
        print("BFS from 1:",planner.graph.bfs(1))
        print("DFS from 1:",planner.graph.dfs(1))
    print("\n--- Dijkstra: Shortest Path 1 -> 6 ---")
    planner.findOptimalPath(1,6)
    print("\n--- Kruskal: Minimum Spanning Tree ---")
    planner.planUtilityLayout()
    print("\n--- Expression Tree: Energy Bill Example ---")
    postfix_example=["base","units","rate","*","+","surcharge","+"]
    vars_example={"base":100,"units":200,"rate":0.12,"surcharge":20}
    planner.evaluateExpression(postfix_example,vars_example)
    print("\n--- Program finished. Capture console screenshots for your report. ---")
