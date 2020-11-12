"""
Tastálacha do Ghaeilge
"""

import os
import re
from NLPGaelach import ga

tests_dir = os.path.dirname(os.path.realpath(__file__))
fixtures_dir = os.path.join(tests_dir, 'fixtures')


def test_it_knows_ga_ipa_fixtures():
    ga_ipa_txt = os.path.join(fixtures_dir, 'ga-ipa.txt')

    with open(ga_ipa_txt) as f:
        for line in f.read().split('\n'):
            entries = re.split(r'\t+', line)

            if line.find('#') != 0 and len(entries) == 2:
                i = entries[0]
                o = entries[1]

                assert ga.to_ipa_str(i) == o
