*********
Consistent-Hashing
*********

**Consistent-Hashing**, as the name says, implements **consistent hashing** in Python.

Consistent hashing is used mostly in Distributed systems/caches/databases/messaging queues as this avoid the total
reshuffling of your key-node mappings when adding or removing a node in your ring. This helps you to cache data in your
servers without worrying much about the slow down or downtime in case of a server failure or addition of removal of
nodes in your application.

Usage
=====
Creating a Ring
-----------
**Consistent-Hashing** is very simple to use:

.. code-block:: python

    from consistent_hashing.ring import Ring

    # create a consistent hash ring of 3 nodes of weight 1
    r = Ring(nodes=[{'key': 'node1'}, {'key': 'node2', 'virtual_nodes': 5}])

    # get the node name for the 'Interstellar' key
    target_node = r.get_node('Interstellar')

Adding / Removing / Updating nodes
-----------
Nodes can be added/removed/updated from your consistent hash ring at any time.

.. code-block:: python
    from consistent_hashing.ring import Ring

    # create a consistent hash ring of 3 nodes of weight 1
    r = Ring(nodes=[{'key': 'node1'}, {'key': 'node2', 'virtual_nodes': 5}])

    # Adds a new node "node3" and updates the configuration for "node1" to have 5 Virtual Nodes instead of 10(default).
    r.configure_nodes([{'key': 'node1', 'virtual_nodes': 5}, {'key': 'node3'}])

    # Removes the nodes passed in the list from the ring.
    r.remove_nodes(['node1'])

Ring options
------------
- **nodes**: Nodes used to create the Ring.
- **hashes**: Stores the hashed values for all the virtual nodes added.
- **ring**: Stores the map of virtual node hashes to their respective node keys.
- **virtual_nodes**: Number of virtual_nodes per node(10 by default).

Available methods (For complete use cases, see docstrings)
-------------
- **configure_nodes([nodes])**: add (or overwrite) the node in the ring with the given config.
- **remove_nodes([node keys])**: Remove the nodes from the ring.
- **get_node(key)**: returns the name of the node for the hashed value of key passed.

Important Links:
===============

- Consistent Hashing: https://en.wikipedia.org/wiki/Consistent_hashing

License
=======
MIT