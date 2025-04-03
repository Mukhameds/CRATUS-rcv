import uuid

# ==== Block ====

class Block:
    def __init__(self, data):
        self.id = str(uuid.uuid4())[:8]
        self.data = data

    def __repr__(self):
        return f"<Block {self.id} | {self.data}>"

# ==== Network ====

class FakeNetwork:
    def __init__(self):
        self.latency = 0.1  # Можем позже добавить задержку

    def send_block(self, from_node, to_node, block):
        print(f"📡 Блок {block.id} от Node {from_node.node_id} -> Node {to_node.node_id}")
        to_node.receive_block(block)

# ==== Node ====

class CratusNode:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.blocks = []
        self.peers = []

    def receive_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            print(f"[Node {self.node_id}] Получен новый блок: {block}")
            self.broadcast_block(block)
        else:
            print(f"[Node {self.node_id}] Уже видел блок {block.id}")

    def broadcast_block(self, block):
        print(f"[Node {self.node_id}] Рассылает блок: {block.id}")
        for peer in self.peers:
            self.network.send_block(self, peer, block)

    def add_peer(self, peer_node):
        self.peers.append(peer_node)

# ==== Main Simulation ====

if __name__ == "__main__":
    # Создание сети
    network = FakeNetwork()

    # Создание узлов
    node_a = CratusNode("A", network)
    node_b = CratusNode("B", network)
    node_c = CratusNode("C", network)

    # Подключение пиров
    node_a.add_peer(node_b)
    node_a.add_peer(node_c)

    node_b.add_peer(node_a)
    node_b.add_peer(node_c)

    node_c.add_peer(node_a)
    node_c.add_peer(node_b)

    # Генерация первого блока (Genesis)
    genesis_block = Block("Genesis Data")
    print("\n🚀 Симуляция запуска: Node A создаёт блок...\n")
    node_a.receive_block(genesis_block)
