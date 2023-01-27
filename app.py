from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('mongodb+srv://davchndra:Davidchandra012@cluster0.5stzdvm.mongodb.net/?retryWrites=true&w=majority')
db = client.wordList


@app.route('/')
def main():
    words_result = db.words.find({}, {'_id': False})
    words = []
    for word in words_result:
        definition = word['definitions'][0]['shortdef']
        definition = definition if type(definition) is str else definition[0]
        words.append({
            'word': word['word'],
            'definition': definition,
        })
    return render_template(
        'index.html',
        words=words
    )


@app.route('/detail/<keyword>')
def detail(keyword):
    api_key = 'd0edcf93-5b8a-473d-a9e5-6f9a4b06c5b8'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()
    return render_template(
        'detail.html',
        word=keyword,
        definitions=definitions,
        status=request.args.get('status_give', 'new')
    )


@app.route('/api/save_word', methods=['POST'])
def save_word():
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    doc = {
        'word': word,
        'definitions': definitions,
    }
    db.words.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': f'Word, {word}, Saved',
    })


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    return jsonify({
        'result': 'success',
        'msg': f'Word, {word}, Deleted'
    })

@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    return jsonify({'result': 'success'})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    return jsonify({'result': 'success'})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)