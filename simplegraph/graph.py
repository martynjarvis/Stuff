import collections
import heapq

class DirectedGraph(object):
    def __init__(self):
        self.graph = collections.defaultdict(dict)

    def add_edge(self,a,b,value):
        self.add_directed_edge(a,b,value)
        self.add_directed_edge(b,a,value)

    def add_directed_edge(self,a,b,value):
        self.graph[a][b] = value

    def remove_directed_edge(self,a,b):
        self.graph[a].pop(b)
        if len(self.graph[a]) == 0:
            self.graph.pop(a)

    def remove_edge(self,a,b):
        self.remove_directed_edge(a,b)
        self.remove_directed_edge(b,a)

    def nodes(self):
        return list(self.graph.keys())

    def links(self, a):
        return self.graph[a]

    def shortest_path(self,source,target):
        '''Dijkstra with priority queue'''
        if source == target:
            return [target]

        distance = {}
        distance[source] = 0
        previous = {}
        q = []  # priority queue with entries [distance, node]
        heapq.heappush(q, [distance[source], source])
        entry_finder = {} # mapping of nodes to queue entries so we can remove tasks
        while len(q) > 0:
            d, u = heapq.heappop(q)
            if u is None:
                continue # this entry has been removed
            assert(d==distance[u])  # sanity check that priority = distance
            for v, length in self.graph[u].iteritems():
                new_dist = d + self.graph[u][v]
                old_dist = distance.get(v,None)
                if old_dist is None or new_dist < old_dist:
                    distance[v] = new_dist
                    previous[v] = u
                    if v in entry_finder:
                        # we've found a shorter path to a node that we've
                        # already seen. Delete old entry.
                        old_entry = entry_finder.pop(v)
                        old_entry[-1] = None # mark old entry as removed
                    entry = [new_dist,v]
                    heapq.heappush(q, entry)
                    entry_finder[v] = entry

        path = [target]
        try:
            while target != source:
                target = previous[target]
                path.append(target)
        except KeyError:
            # unconnected graph
            return None
        path.reverse()
        return path
