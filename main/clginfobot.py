from django import template
from django.conf.urls.static import static
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow as tf
import json
import pickle
import datetime
import random

stemmer = LancasterStemmer()
with open("static/clginfobot/intents.json") as file:
    data = json.load(file)

with open("static/clginfobot/data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)

model.load("static/clginfobot/model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def response(inp):
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    response.tagg = tag
    if results[results_index] > 0.5:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                contexts = tg['context_set']
        response.contextimg = random.choice(contexts)
        rresponse = random.choice(responses)
        print(rresponse)
    else:
        rresponse = "PLEASE GIVE A VALID QUESTION"
        response.contextimg = "./static/context/images/error.gif"
        file.close()

        if inp == "":
            pass
        else:
            intents_template = {
              "tag": "",
              "patterns": [],
              "responses": [],
              "context_set": [""]
            }
        
            update_tag = {"tag": inp}
            update_patterns = {"patterns": [str(inp)]}
            update_responses = {"responses":["answer need to be provided"]}
    
            intents_template.update(update_tag)
            intents_template.update(update_patterns)
            intents_template.update(update_responses)
    
            def write_json(new_data, filename='static/clginfobot/intents.json'):
                with open(filename,'r+') as file1:
                      # First we load existing data into a dict.
                    file_data = json.load(file1)
                    # Join new_data with intents.json inside intents
                    file_data["intents"].append(new_data)
                    # Sets file's current position at offset.
                    file1.seek(0)
                    # convert back to json.
                    json.dump(file_data, file1, indent = 4)
            write_json(intents_template)

    return rresponse

 
