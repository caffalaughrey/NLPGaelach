"""
Tastálacha do Ghaeilge Mhanainn
"""

import os
import re
from NLPGaelach import gv

tests_dir = os.path.dirname(os.path.realpath(__file__))
fixtures_dir = os.path.join(tests_dir, 'fixtures')


def test_it_knows_gv_ipa_fixtures():
    gv_ipa_txt = os.path.join(fixtures_dir, 'gv-ipa.txt')

    with open(gv_ipa_txt) as f:
        for line in f.read().split('\n'):
            entries = re.split(r'\t+', line)

            if line.find('#') != 0 and len(entries) == 2:
                i = entries[0]
                o = entries[1]

                assert gv.to_ipa_str(i) == o
