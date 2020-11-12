PUNCTUATION = ['\'', '"', '-']


class Graph:
    def __init__(self, value, token):
        self.value = value
        self.token = token
        self.previous = None
        self.next = None
        self.is_broad = None
        self.is_slender = None
        self.ipa = None

    def is_consonant(self):
        pass # Must implement

    def is_vowel(self):
        pass # Must implement

    def is_final_sound(self):
        pass # must implement

    def is_punctuation(self):
        return self.value in PUNCTUATION

    def walk(self, fn, **kwargs):
        next = self.next
        cont = fn(self, **kwargs)

        if next is not None and cont is True:
            return next.walk(fn, **kwargs)
        else:
            return True

    def revwalk(self, fn, **kwargs):
        previous = self.previous
        cont = fn(self, **kwargs)

        if previous is not None and cont is True:
            return previous.revwalk(fn, **kwargs)
        else:
            return True


def get_graphs(value, token, graphs, all_possible_values, cls=Graph, index=0):
    original_index = index

    if len(value) == 0:
        return graphs

    for possible_graph in all_possible_values:
        if value.find(possible_graph) == index:
            graphs.append(cls(possible_graph, token))

            index = index + len(possible_graph)

            break

    if index == original_index:
        # print('No graph found for "%s"' % value) # TODO: use actual logging

        return get_graphs(value[1:], token, graphs, all_possible_values, cls)
    elif index == len(value):
        return graphs
    else:
        return get_graphs(value[index:], token, graphs, all_possible_values, cls)
