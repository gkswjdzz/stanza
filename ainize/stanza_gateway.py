from flask import Flask, request, abort, jsonify, redirect
import json
import os
import requests

from prepare_resources import default_treebanks, lcode2lang

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def annotate():
  print('new input')
  keys = list(request.form.keys())

  if len(keys) != 2 :
    return jsonify({'message': 'invalid body'}), 400
  
  text_key = list(request.form.keys())[0]
  lang_key = list(request.form.keys())[1]
  
  text = request.form[text_key]
  lang = request.form[lang_key]

  lang_list =list(default_treebanks.keys())
  if lang not in lang_list:
    return jsonify({'message': 'invalid language'}), 400
  
  if len(text) == 0 :
    return jsonify({'message': 'no text'}), 400

  print(lang, text)
  idx = lang_list.index(lang)
  
  lang2lcode = { v: k for k, v in lcode2lang }

  data = {
    'sentences' : text,
    'lcode' : lang2lcode[lang]
  }
  
  server_id = int(idx / 10)
  url = f'https://stanza-{server_id}.gkswjdzz.endpoint.ainize.ai/analyze'
  
  print(f'server id : {server_id}, {url}')
  res = requests.post(url, data=data)

  if res.status_code != 200:
    return jsonify({'message':'invalid requests'}), res.status_code
  
  print('OK')
  return res.json(), 200

if __name__ == "__main__":
  app.run(debug=False, port=80, host='0.0.0.0')