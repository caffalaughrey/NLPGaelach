import argparse
from NLPGaelach import gv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ga', action='store_true', help='Bain úsáid as uirlisí Ghaeilge na hÉireann / Use Irish tools')
    parser.add_argument('--gd', action='store_true',
                        help='Bain úsáid as uirlisí Ghaeilge na hAlban / Use Scottish tools')
    parser.add_argument('--gv', action='store_true', help='Bain úsáid as uirlisí Ghaeilge Mhanann / Use Manx tools')
    parser.add_argument('--ipa', help='Teaghrán le rangú mar luach IPA / String to classify as an IPA value')

    args = parser.parse_args()
    is_gv = args.gv
    ipa = args.ipa

    if is_gv is True:
        if ipa is not None:
            print(gv.to_ipa_str(ipa))

            exit()

    parser.print_help()
