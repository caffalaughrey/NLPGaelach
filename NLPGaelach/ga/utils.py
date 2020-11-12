def eval_short_a(graph):
    # / a /
    # patrún
    # samplaí
    # a     cas, fan, tar
    # ai    baile
    # ea    eala, fear, bean
    value = graph.value

    return 'a' if value == 'a' or value == 'ai' or value == 'ea' else None


def eval_long_a(graph):
    # / a: /
    # patrún
    # samplaí
    # á     gá, bá, pá
    # a, ai, or ea before ll, m, nn, or rr  am, caill, fearr, gearr
    # a, or ai before rd, rl, rn    ard, tharla, tairne
    value = graph.value

    # TODO: Add lookahead logic for ll, m, nn, rr, rd, rl, and rd
    return 'aː' if value == 'á' else None


def eval_ai(graph):
    # / ai /
    # patrún
    # samplaí
    # adh   adharc, gadhar
    # agh   laghad, aghaidh
    # eidh  eidhneán
    # aidh  aidhm
    # aigh  aighneas
    value = graph.value

    return 'ai' if value == 'adh' or value == 'agh' or value == 'eidh' or value == 'aidh' or value == 'aigh' else None


def eval_au(graph):
    # /au/
    # patrún	samplaí
    # abh	gabhar
    # amh	ramhar, samhradh
    # odh	bodhar
    # ogh	rogha
    value = graph.value

    return 'au' if value == 'abh' or value == 'amh' or value == 'odh' or value == 'ogh' else None


def eval_short_e(graph):
    # /e/
    # patrún	samplaí
    # ei	meicneoir, teicneolaíocht, feiceáil
    return 'e' if graph.value == 'ei' or graph.value == 'e' else None


def eval_long_e(graph):
    # /e:/
    # patrún	samplaí
    # é	pé, mé, sé
    # éa	éan, méar
    # éi	Éire, péire, féirín
    # ae	aer
    # aei	Gaeilge
    value = graph.value

    return 'eː' if value == 'é' or value == 'éa' or value == 'éi' or value == 'ae' or value == 'aei' else None


def eval_ei(graph):
    # /ei/
    # patrún	samplaí
    # -eidh	beidh
    next = graph.next
    previous = graph.previous
    value = graph.value

    if previous is None:
        return None
    elif value == 'eidh' and previous is not None and previous.value == 'b' and previous.previous is None and \
            next is None:
        return 'ei'


def eval_short_i(graph):
    # /i/
    # patrún	samplaí
    # i	in, iris, ispín
    # io	sliotar
    # oi	oileán
    # ui	fuinneog
    return 'i' if graph.value == 'i' or graph.value == 'io' or graph.value == 'oi' or graph.value == 'ui' else None


def eval_long_i(graph):
    # /i:/
    # patrún	samplaí
    # í	bí, go dtí, íseal
    # ao	taobh
    # aoi	aois
    value = graph.value
    long_i_values = ['í', 'aí', 'aío', 'ao', 'aoi', 'uí', 'uío']

    return 'iː' if value in long_i_values else None


def eval_i_schwa(graph):
    # /iə/
    # patrún	samplaí
    # ia	ciall, bia, iasc
    return 'iə' if graph.value == 'ia' else None


def eval_short_o(graph):
    # /o/
    # patrún	samplaí
    # o	bog, lom, borradh
    return 'o' if graph.value == 'o' else None


def eval_long_o(graph):
    # /o:/
    # patrún	samplaí
    # ó	bó, a dó
    # eo	eorna, eolas
    # omh	comhairle, comhar
    return 'oː' if graph.value == 'ó' or graph.value == 'eo' or graph.value == 'omh' else None


def eval_short_u(graph):
    # /u/
    # patrún	samplaí
    # u	rud, ar fud, dubh
    return 'u' if graph.value == 'u' else None


def eval_schwa(graph):
    # /ə/
    # patrún	samplaí
    # -a	tada, hata
    # -e	baile, file
    # a- in certain positional or time-related words	anuas, anseo, aréir
    # -adh in verbal nouns	bualadh, casadh
    # TODO: All of the above patterns
    pass


def eval_long_u(graph):
    # /uː/
    # patrún	samplaí
    # ú	clúmhach, dúshlán, sú
    # umh	an Mhumhain, ciumhais, umha
    return 'uː' if graph.value == 'ú' or graph.value == 'umh' else None


def eval_u_schwa(graph):
    # /uə/
    # patrún	samplaí
    # ua	fuar, bua
    return 'uə' if graph.value == 'ua' else None


vowel_model = [
    eval_schwa,
    eval_long_a,
    eval_ei,
    eval_short_a,
    eval_ai,
    eval_au,
    eval_short_e,
    eval_long_e,
    eval_short_i,
    eval_long_i,
    eval_i_schwa,
    eval_short_o,
    eval_long_o,
    eval_short_u,
    eval_long_u,
    eval_u_schwa
]


def eval_vowel(graph):
    for classifier in vowel_model:
        ipa = classifier(graph)

        if ipa is not None:
            return ipa


def strip_consonants(x):
    return ''.join(c for c in x if c in 'aáeéiíoóuú')
