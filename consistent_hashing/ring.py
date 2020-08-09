import hashlib
import bisect


class Ring(object):
    """
    Consistent hash ring.
    Returns Ring object with the nodes configured. Configuration of a node to be passed:
    {
        "key": "< value of the key >",
        "virtual_nodes": "< Number of virtual nodes >"
        "< Any other key you want to keep, for example, say server config - PORT, HOST, etc>": < Value of key added >
    }
    Can use the following attributes to access the:
    - ring - To access the map of hashed values of virtual nodes to node keys.
    - hashes - To access the sorted hashed values of virtual nodes.
    - nodes - To access the map of node keys to their configuration in the ring.

    Following methods can be run to update the ring:
    - configure_nodes - To update the configuration of nodes in the ring. Can be used to add/update nodes in the ring.
    - remove nodes - To remove the nodes from the ring.
    - get_node - To get the node where a particular key should reside.
    """

    def __init__(self, nodes, **kwargs):
        self.nodes = {}
        self.hashes = []
        self.virtual_nodes =  kwargs.get('virtual_nodes', 10)
        self.ring_map = {}
        self.configure_nodes(nodes)

    def _get_hash(self, key):
        """
        Generate MD5 hash for the key passed.
        :param key: Key
        :return: hashed value
        """
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def configure_nodes(self, nodes):
        """
        Method to configure new/existing nodes in the ring.
        :param (List) nodes: List of dicts new/existing nodes with complete configuration.
        """
        for node in nodes:
            existing_node = self.nodes.get(node['key'])
            if existing_node:
                new_virtual_nodes = node.get('virtual_nodes', self.virtual_nodes)
                self.update_nodes(existing_node, new_virtual_nodes, node)
                existing_node["virtual_nodes"] = new_virtual_nodes
            else:
                virtual_nodes = node.get('virtual_nodes', self.virtual_nodes)
                for virtual_node in range(virtual_nodes):
                    self._add_vnode(virtual_node, node['key'])
                self.nodes[node['key']] = node

    def remove_nodes(self, nodes):
        """
        Remove nodes from the ring.
        :param nodes: List of keys of nodes to be removed.
        """
        to_be_deleted_nodes = [
            existing_node for new_node in nodes for existing_node in self.nodes if new_node == existing_node
        ]
        for node in to_be_deleted_nodes:
            virtual_nodes = self.nodes[node].get('virtual_nodes', self.virtual_nodes)
            for virtual_node in range(virtual_nodes):
                self._remove_vnode(virtual_node, node)
            del self.nodes[node]

    def _remove_vnode(self, vnode, key):
        """
        Internal utility method to remove a virtual node from the ring.
        :param (Integer) vnode: Virtual node to be deleted.
        :param (Strig) key: Key of node from which virtual node is to be deleted.
\        """
        hashed_val = self._get_hash('{}_{}'.format(key, vnode))
        del self.ring_map[hashed_val]
        self.hashes.remove(hashed_val)

    def _add_vnode(self, vnode, key):
        """
        Internal utility method to add a virtual node from the ring.
        :param (Integer) vnode: Virtual node to be deleted.
        :param (Strig) key: Key of node from which virtual node is to be deleted.
        """
        hashed_val = self._get_hash('{}_{}'.format(key, vnode))
        self.ring_map[hashed_val] = key
        bisect.insort(self.hashes, hashed_val)

    def update_nodes(self, existing_node, new_virtual_nodes, new_node):
        """
        Internal utility method to update existing nodes.
        :param existing_node: Existing node to be updated.
        :param new_virtual_nodes: New virtual ndoes.
        :param new_node: New node configuration.
        """
        existing_virtual_nodes = existing_node.get('virtual_nodes', self.virtual_nodes)
        if existing_virtual_nodes != new_virtual_nodes:
            if existing_virtual_nodes > new_virtual_nodes:
                for n in range(new_virtual_nodes, existing_virtual_nodes):
                    self._remove_vnode(new_node['key'], n)
            else:
                for virtual_node in range(existing_virtual_nodes, new_virtual_nodes):
                    self._add_vnode(virtual_node, new_node['key'])

    def get_node(self, val):
        """
        Method to get the node where the value should reside.
        :param val: Value to be checked
        :return: node value
        """
        pos = bisect.bisect(self.hashes, self._get_hash(val))
        if pos == len(self.hashes):
            pos = 0
        return self.ring_map[self.hashes[pos]]
