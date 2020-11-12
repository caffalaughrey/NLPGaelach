# NLPGaelach
Uirlisí NLP do na teangacha gaelacha.

## Riachtanais
* [Python 3.7](https://www.python.org/downloads/)
* [virtualenv](https://pypi.org/project/virtualenv/)

## Cuir tús leis
### Cruthaigh timpeallacht fhiorúil
Tar éis an stór (*repo*) seo a chlónáil, cruthaigh timpeallacht fhíorúil Python le:

```bash
python -m venv .virtualenv
```

### Cuir an timpeallacht fhíorúil i ngníomh
Anois cuir an timpeallacht fhíorúil i ngníomh. Ar chórais macOS, Linux agus Unix, rith:

```bash
source .virtualenv/bin/activate
```

...nó ar Windows, rith:

```bash
.virtualenv\Scripts\activate.bat
```

### Suiteáil
Chun an pacáiste a shuiteáil, rith:

```bash
pip install .
```

## Tastáil
Is féidir tástalacha aonaid a rith trí setup.py le:

```bash
python setup.py test
```

## Doicimeádúchán
Chun doiciméadúchán Sphinx a ghineadh, rith:

```bash
python setup.py doc
```

Ansin beidh an doiciméadúchán ar fáil in `docs/_build`.
