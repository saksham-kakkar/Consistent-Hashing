import random
import string
import unittest

from consistent_hashing.ring import Ring


def random_string(length=10):
    """Generate a random string of fixed length """
    values = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(values) for _ in range(length))


class ConsistentHashingRingtest(unittest.TestCase):
    """
    Tests for Consistent Hashing Ring.
    """
    def test_ring(self):
        no_of_keys = 1000
        no_of_nodes = 100
        nodes = [{'key': 'node{}'.format(n)} for n in range(0, no_of_nodes)]
        ring_obj = Ring(nodes)
        distributions = {}
        for key in range(no_of_keys):
            s = random_string()
            node = ring_obj.get_node(s)
            distributions[node] = distributions.get(node, 0) + 1
        self.assertEqual(len(ring_obj.hashes), 100 * 10)
        self.assertEqual(len(ring_obj.ring_map), 100 * 10)
        self.assertEqual(sum(distributions.values()), no_of_keys)
        self.assertTrue(max(distributions.values()) < 200)  # Max value should be less than 1/5th


    def test_different_virtual_nodes(self):
        no_of_nodes = 100
        nodes = [{'key': 'node{}'.format(n), 'virtual_nodes': n} for n in range(0, no_of_nodes)]
        ring_obj = Ring(nodes)
        self.assertEqual(len(ring_obj.hashes), 99 * 100 / 2)  # sum of values from 1 to n = n*(n+1)/2


if __name__ == '__main__':
    unittest.main()