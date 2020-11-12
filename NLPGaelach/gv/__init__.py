import nltk

from ..graphs import Graph, get_graphs, PUNCTUATION
from ..tokens import Token
from .constants import *
from .utils import guess_length


class GraphGV(Graph):
    def __init__(self, value, token):
        super().__init__(value, token)

        self.is_final_silent_e = None
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

        if self.is_final_silent_e:
            return False
        elif next is not None and next.is_final_silent_e:
            return True
        elif next is None or next.value == '-':
            return True

        return False


class TokenGV(Token):
    def get_graphs(self):
        if self.graphs is None:
            all_possible_graphs = ALL_POSSIBLE_GRAPHS + PUNCTUATION
            graphs = self.graphs = get_graphs(self.value.lower(), self, [], all_possible_graphs, GraphGV)

            pre_classify(graphs)
            classify(graphs)

        return self.graphs

    def syllable_count(self):
        count = 0

        graphs = self.get_graphs()

        for graph in graphs:
            if graph.is_vowel() and graph.is_final_silent_e is False:
                count = count + 1

        return count


def pre_classify(graphs):
    is_stress_classified = False

    for index in range(len(graphs)):
        current = graphs[index]
        previous = None if index - 1 < 0 else graphs[index - 1]
        next = None if index + 1 == len(graphs) else graphs[index + 1]

        current.previous = previous
        current.next = next
        current.is_final_silent_e = True if (current.value == 'e' and index + 1 == len(graphs)) or \
                                            (next is not None and next.value == '-' and current.value == 'e') else False

        if current.is_vowel() and is_stress_classified is False:
            current.is_stressed = True
            is_stress_classified = True


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

    def classify_final_e_vowel(graph):
        if graph.is_vowel() and not graph.is_final_silent_e:
            value = graph.value
            ipa = graph.ipa = FINAL_E_VOWELS[value]
            is_broad = graph.is_broad = guess_length(ipa, 'broad')
            is_slender = graph.is_slender = guess_length(ipa, 'slender')
            previous = graph.previous

            if previous is not None:
                kwargs = {"is_broad": is_broad, "is_slender": is_slender}
                previous.revwalk(fan_consonant_lengths, **kwargs)

            return False
        elif graph.is_punctuation():
            return False
        else:
            return True

    def classify_known_consonant_lengths(graph):
        value = graph.value

        if graph.is_consonant():
            if value in UNIQUE_BROAD_CONSONANTS:
                ipa = BROAD_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)
                graph.is_broad = True
            elif value in UNIQUE_SLENDER_CONSONANTS:
                ipa = SLENDER_CONSONANTS[value]
                graph.ipa = ipa if type(ipa) is str else ipa(graph)
                graph.is_slender = True

            if graph.ipa is not None:
                is_broad = graph.is_broad
                is_slender = graph.is_slender
                kwargs = {"is_broad": is_broad, "is_slender": is_slender}

                graph.walk(fan_consonant_lengths, **kwargs)
                graph.revwalk(fan_consonant_lengths, **kwargs)

        return True

    def classify_vowels(graph):
        value = graph.value

        if graph.is_vowel() and graph.is_final_silent_e is False and graph.ipa is None:
            ipa = ORD_VOWELS[value]
            ipa = graph.ipa = ipa if type(ipa) is str else ipa(graph)
            is_broad = graph.is_broad = guess_length(ipa, 'broad')
            is_slender = graph.is_slender = guess_length(ipa, 'slender')
            previous = graph.previous

            if previous is not None:
                kwargs = {"is_broad": is_broad, "is_slender": is_slender}
                previous.revwalk(fan_consonant_lengths, **kwargs)

        return True

    def classify_final_consonants(graph):
        if graph.is_final_silent_e:
            return True
        elif graph.ipa is not None:
            is_broad = graph.is_broad
            is_slender = graph.is_slender
            kwargs = {"is_broad": is_broad, "is_slender": is_slender}
            next = graph.next
            previous = graph.previous

            if not graph.is_vowel() and previous is not None:
                previous.revwalk(fan_consonant_lengths, **kwargs)

            if next is not None:
                next.walk(fan_consonant_lengths, **kwargs)

            return False
        else:
            return True

    def reclassify_schwa_consonants(graph):
        next = graph.next
        previous = graph.previous
        value = graph.value

        if next is None or previous is None:
            return True
        elif graph.is_consonant() and next.ipa == 'ə' and previous.is_slender and not graph.is_slender and \
                value in SLENDER_CONSONANTS:
            graph.is_slender = True
            graph.is_broad = False
            ipa = SLENDER_CONSONANTS[value]
            graph.ipa = ipa if type(ipa) is str else ipa(graph)

        return True

    if len(graphs) > 0:
        lasts = [graph for graph in graphs if (graph.next is not None and graph.next.value == '-')
                 or graph.next is None]
        for last in lasts:
            if last.is_final_silent_e:
                last.revwalk(classify_final_e_vowel)

        graphs[0].walk(classify_known_consonant_lengths)
        graphs[0].walk(classify_vowels)

        for last in lasts:
            if last.is_consonant() or last.is_final_silent_e:
                last.revwalk(classify_final_consonants)

        graphs[0].walk(reclassify_schwa_consonants)


def to_ipa_str(s):
    tokens = nltk.word_tokenize(s)
    ipas = []

    for token in tokens:
        token = TokenGV(token)

        if token.syllable_count() > 0:
            ipas.append(token.get_ipa())

    return ' '.join(ipas)
