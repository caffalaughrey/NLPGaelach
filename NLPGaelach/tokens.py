class Token:
    def __init__(self, value):
        self.value = value
        self.graphs = None

    def get_graphs(self):
        pass # Must implement

    def get_ipa(self):
        ipas = [graph.ipa for graph in self.get_graphs() if graph.ipa is not None]

        return ''.join(ipas)

    def syllable_count(self):
        pass # Must implement

    def pre_classify(self):
        pass # Must implement

    def classify(self):
        pass # Must implement
