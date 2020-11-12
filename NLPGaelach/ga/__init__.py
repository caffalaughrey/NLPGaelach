import nltk

from ..graphs import Graph, get_graphs, PUNCTUATION
from ..tokens import Token
from .constants import *
from .utils import eval_vowel, strip_consonants


class GraphGA(Graph):
    def __init__(self, value, token):
        super().__init__(value, token)

        self.is_stressed = False

    def is_between_vowels(self):
        next = self.next
        previous = self.previous

        if next is not None and previous is not None:
            return next.is_vowel() and previous.is_vowel()

        return False

    def is_consonant(self):
        return self.value in POSSIBLE_CONSONANTS

    def is_vowel(self):
        return self.value in POSSIBLE_VOWELS

    def is_final_sound(self):
        next = self.next

        if next is None or next.value == '-':
            return True

        return False


class TokenGA(Token):
    def get_graphs(self):
        if self.graphs is None:
            all_possible_graphs = ALL_POSSIBLE_GRAPHS + PUNCTUATION
            graphs = self.graphs = get_graphs(self.value.lower(), self, [], all_possible_graphs, GraphGA)

            pre_classify(graphs)
            classify(graphs)

        return self.graphs

    def syllable_count(self):
        count = 0

        graphs = self.get_graphs()
        vowels = [graph.value for graph in graphs if graph.is_vowel()]

        return len(vowels)


def pre_classify(graphs):
    is_stress_classified = False

    for index in range(len(graphs)):
        current = graphs[index]
        previous = None if index - 1 < 0 else graphs[index - 1]
        next = None if index + 1 == len(graphs) else graphs[index + 1]

        current.previous = previous
        current.next = next

        if current.is_vowel() and is_stress_classified is False:
            current.is_stressed = True
            is_stress_classified = True
        elif current.is_consonant() and next is not None and next.is_vowel():
            current.is_broad = next.value[0] in ['a', 'á', 'o', 'ó', 'u', 'ú']
            current.is_slender = next.value[0] in ['i', 'í', 'e', 'é']


def classify(graphs):
    def fan_consonant_lengths(graph, **kwargs):
        value = graph.value
        is_broad = kwargs.get('is_broad')
        is_slender = kwargs.get('is_slender')

        if graph is None or graph.is_vowel() or graph.is_punctuation():
            return False
        elif graph.ipa is None:
            graph.is_broad = is_broad
            graph.is_slender = is_slender

            if is_broad:
                ipa = BROAD_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)
            elif is_slender:
                ipa = SLENDER_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)

        return True

    def classify_known_consonant_lengths(graph):
        value = graph.value

        if graph.is_consonant():
            if graph.is_broad:
                ipa = BROAD_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)
            elif graph.is_slender:
                ipa = SLENDER_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)

            if graph.ipa is not None:
                is_broad = graph.is_broad
                is_slender = graph.is_slender
                kwargs = {"is_broad": is_broad, "is_slender": is_slender}

                graph.walk(fan_consonant_lengths, **kwargs)
                graph.revwalk(fan_consonant_lengths, **kwargs)

        return True

    def classify_vowels(graph):
        value = graph.value

        if graph.is_vowel() and graph.ipa is None:
            ipa = eval_vowel(graph)

            if ipa is not None:
                graph.ipa = ipa if type(ipa) is str else ipa(graph)

        return True

    def classify_final_consonants(graph):
        next = graph.next
        previous = graph.previous
        value = graph.value

        if graph.is_consonant() and previous is not None and previous.is_vowel():
            vowel = strip_consonants(previous.value)
            lastchar = '' if len(vowel) <= 0 else previous.value[len(vowel)-1]
            is_broad = graph.is_broad = vowel.endswith('ae') or lastchar in ['a', 'á', 'o', 'ó', 'u', 'ú']
            is_slender = graph.is_slender = True if not is_broad and lastchar in ['i', 'í', 'e', 'é'] else False
            kwargs = {"is_broad": is_broad, "is_slender": is_slender}

            if is_broad:
                ipa = BROAD_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)
            elif is_slender:
                ipa = SLENDER_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)

            if previous is not None:
                previous.revwalk(fan_consonant_lengths, **kwargs)

            if next is not None:
                next.walk(fan_consonant_lengths, **kwargs)

            return False
        elif graph.is_vowel():
            return False
        else:
            return True

    if len(graphs) > 0:
        lasts = [graph for graph in graphs if (graph.next is not None and graph.next.value == '-')
                 or graph.next is None]

        graphs[0].walk(classify_known_consonant_lengths)
        graphs[0].walk(classify_vowels)

        for last in lasts:
            last.revwalk(classify_final_consonants)


def to_ipa_str(s):
    tokens = nltk.word_tokenize(s)
    ipas = []

    for token in tokens:
        token = TokenGA(token)

        if token.syllable_count() > 0:
            ipas.append(token.get_ipa())

    return ' '.join(ipas)
