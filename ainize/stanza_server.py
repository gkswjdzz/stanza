from flask import Flask, request, abort, jsonify
import json
import stanza
import os
import argparse

from prepare_resources import default_treebanks

app = Flask(__name__)

pipelineCache = dict()

@app.route('/analyze', methods=['POST'])
def annotate():
  global pipelineCache

  keys = list(request.form.keys())

  if len(keys) != 2 :
    return jsonify({'message': 'invalid body'}), 400
  
  text_key = list(request.form.keys())[0]
  lang_key = list(request.form.keys())[1]
  
  text = request.form[text_key]
  lang = request.form[lang_key]
  print(text, lang)
  
  if len(text) == 0 :
    return jsonify({'message': 'no text'}), 400
  
  if lang not in list(default_treebanks.keys()):
    return jsonify({'message': 'invalid lang'})
    
  if lang not in pipelineCache:
    stanza.download(lang)
    pipelineCache[lang] = stanza.Pipeline(lang=lang, use_gpu=False)

  res = pipelineCache[lang](text)

  annotated_sentences = []
  for sentence in res.sentences:
    tokens = []
    deps = []
    for word in sentence.words:
      tokens.append({'index': word.id, 'word': word.text, 'lemma': word.lemma, 'pos': word.xpos, 'upos': word.upos, 'feats': word.feats, 'ner': word.parent.ner if word.parent.ner is None or word.parent.ner == 'O' else word.parent.ner[2:]})
      deps.append({'dep': word.deprel, 'governor': word.head, 'governorGloss': sentence.words[word.head-1].text,
        'dependent': word.id, 'dependentGloss': word.text})
    annotated_sentences.append({'basicDependencies': deps, 'tokens': tokens})

  return jsonify({'sentences': annotated_sentences}), 200

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--server')
  args = parser.parse_args()
  args.server = int(args.server)

  end = None 
  list_banks = list(default_treebanks.keys())

  if (args.server + 1) * 10 < len(list_banks):
    end = (args.server + 1) * 10
  else:
    end = len(list_banks)
  start = args.server * 10

  print(start, end)
  for lang in list_banks[start:end]:
    pipelineCache[lang] = stanza.Pipeline(lang=lang, dir='./models', use_gpu=False)

  app.run(debug=False, port=80, host='0.0.0.0', threaded=False)