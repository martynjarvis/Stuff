import unittest

from simplegraph.graph import DirectedGraph

class DirectedGraphTest(unittest.TestCase):
    def test_add_directed_edge(self):
        n = DirectedGraph()
        n.add_directed_edge('a','b',1)
        n.add_directed_edge('b','c',2)
        n.add_directed_edge('c','a',3)

        self.assertEqual(n.links('a'), {'b':1})
        self.assertEqual(n.links('b'), {'c':2})
        self.assertEqual(n.links('c'), {'a':3})

    def test_add_edge(self):
        # simple line DirectedGraph
        n = DirectedGraph()
        n.add_edge('a','b',1)
        n.add_edge('b','c',2)
        n.add_edge('c','d',3)

        self.assertEqual(sorted(n.nodes()), ['a','b','c','d'])
        self.assertEqual(n.links('a'), {'b':1})
        self.assertEqual(n.links('b'), {'a':1, 'c':2})
        self.assertEqual(n.links('c'), {'b':2, 'd':3})
        self.assertEqual(n.links('d'), {'c':3})

    def test_remove_edge(self):
        # triange DirectedGraph
        n = DirectedGraph()
        n.add_edge('a','b', 1)
        n.add_edge('b','c', 1)
        n.add_edge('c','a', 1)
        n.remove_edge('a','c')

        self.assertEqual(sorted(n.nodes()), ['a','b','c'])
        self.assertEqual(n.links('a'), {'b':1})
        self.assertEqual(n.links('b'), {'a':1,'c':1})
        self.assertEqual(n.links('c'), {'b':1})

    def test_shortest_path(self):
        # hexagon with path through middle
        n = DirectedGraph()
        n.add_edge('a','b', 1)
        n.add_edge('b','c', 1)
        n.add_edge('c','d', 1)
        n.add_edge('d','e', 1)
        n.add_edge('e','f', 1)
        n.add_edge('f','a', 1)

        n.add_edge('c','f', 2)

        self.assertEqual(n.shortest_path('a','b'), ['a','b'])
        self.assertEqual(n.shortest_path('a','d'), ['a','b','c','d'])

    def test_shortest_path_lengths(self):
        n = DirectedGraph()
        n.add_edge('a','b', 1)
        n.add_edge('b','c', 1)
        n.add_edge('c','a', 5)

        self.assertEqual(n.shortest_path('a','c'), ['a','b','c'])

    def test_shortest_path_directed(self):
        n = DirectedGraph()
        n.add_directed_edge('a','b', 1)
        n.add_directed_edge('b','c', 1)
        n.add_directed_edge('c','a', 1)

        self.assertEqual(n.shortest_path('a','c'), ['a','b','c'])

    def test_disconnected_graph(self):
        n = DirectedGraph()
        n.add_edge('a','b',1)

        n.add_edge('x','y',1)
        n.add_edge('y','z',2)
        n.add_edge('z','x',3)

        self.assertEqual(n.shortest_path('a','x'), None)
