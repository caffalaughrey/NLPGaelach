def guess_length(ipa, length):
    is_slender = False

    for char in ['i', 'iː', 'e', 'eː']:
        if ipa.find(char) == 0:
            is_slender = True

            break

    if length == 'slender':
        return is_slender
    elif length == 'broad':
        return not is_slender


def s_ipa_fn(graph):
    next = graph.next
    precedes_n = True if next is not None and next.value == 'n' else False

    if precedes_n:
        return 'ʃ'
    elif graph.is_between_vowels():
        return 'z'
    else:
        return 's'
