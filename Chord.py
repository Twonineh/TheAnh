import hashlib

class ChordNode:
    def __init__(self, node_id, max_id=16):
        self.node_id = node_id
        self.successor = None
        self.predecessor = None
        self.finger_table = []
        self.max_id = max_id

    def __repr__(self):
        return f"Node({self.node_id})"

    def hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.max_id

    def update_finger_table(self, nodes):
        self.finger_table = nodes

class Chord:
    def __init__(self, num_nodes=4, max_id=16):
        self.nodes = []
        self.max_id = max_id
        self.num_nodes = num_nodes

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.node_id)
        self._update_successors_and_predecessors()

    def _update_successors_and_predecessors(self):
        for i, node in enumerate(self.nodes):
            node.predecessor = self.nodes[i - 1] if i > 0 else self.nodes[-1]
            node.successor = self.nodes[i + 1] if i + 1 < len(self.nodes) else self.nodes[0]
            node.update_finger_table(self.nodes)

    def find_node(self, key):
        hashed_key = key
        print(f"Searching for key: {key} (hashed value: {hashed_key})")
        
        start_node = self.nodes[0]
        current_node = start_node
        
        while True:
            next_node = None
            for finger in current_node.finger_table:
                if finger.node_id >= hashed_key:
                    next_node = finger
                    break
            if not next_node:
                next_node = current_node.successor
            if next_node.node_id >= hashed_key:
                return next_node
            current_node = next_node

    def display_ring(self):
        print("Chord Ring State:")
        for node in self.nodes:
            print(f"Node {node.node_id} -> Predecessor: {node.predecessor.node_id} | Successor: {node.successor.node_id}")

def test_chord():
    chord = Chord(num_nodes=4, max_id=16)
    node_ids = [1, 4, 8, 12]  # N1, N2, N3, N4
    for node_id in node_ids:
        node = ChordNode(node_id)
        chord.add_node(node)
    
    chord.display_ring()
    
    key_to_find = 10
    responsible_node = chord.find_node(key_to_find)
    print(f"\nNode responsible for key {key_to_find}: {responsible_node}")

test_chord()
