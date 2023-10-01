import pymorphy2

from nltk.tokenize import word_tokenize

def parse_token(token, morph):
    res = {}
    for p in morph.parse(token):
        key = (p.normal_form, p.tag.POS)
        if key not in res:
            res[key] = [ p ]
        else:
            res[key].append(p)
    return res

def parse_sentence(sentence, morph):
    tokens = word_tokenize(sentence, language='russian')
    return { token : parse_token(token, morph) for token in tokens }

def print_normalisation(sentence_parsed):
    for token, normals in sentence_parsed.items():
        normals_list = [f"{normal} ({POS})" for normal, POS in normals.keys()]
        normals_str = ", ".join(normals_list)

        token += ":"
        print(f"{token:<15}{normals_str}")