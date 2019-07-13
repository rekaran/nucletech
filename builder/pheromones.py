import pandas as pd
import numpy as np
# from numpy import *
import sys
import json
import re

tmp_dataset = {
    "greetings": ["Hello", "Hi", "Greetings!", "Hi, How is it going?", "How are you doing?", "Nice to meet you.", "How do you do?", "Hi, nice to meet you.", "It is a pleasure to meet you.", "Top of the morning to you!", "What's up?"],
    "name_st": ["My name is #name", "you can call me #name", "I am #name", "#name is my name", "is #name my name"],
    "what_ques": ["what is #your_name", "what is #product"],
    "who_ques": ["who is #name"],
    "how_ques": ["How are you", "How will #product help me"]
}

def tokenize(data):
    rgx = re.compile(r"[#\w']+")
    word_list = rgx.findall(data)
    word_list = [w.lower() for w in word_list]
    # print(word_list)
    return word_list

def mlVocab(dataset):
    vocab = []
    ner_dicts = {}
    for key, data in dataset.items():
        for d in data:
            token = tokenize(d)
            vocab+=token
            ner_list = [n for n in token if n[0]=="#"]
            if len(ner_list)>0:
                ner_dicts[key] = ner_list
    vocab = list(sorted(set(vocab)))
    return vocab, ner_dicts

def mlTensor(dataset):
    vocab, ner_dicts = mlVocab(dataset)
    len_vocab = len(vocab)
    intent = list(dataset.keys())
    tensor_word = np.zeros([len_vocab, len_vocab], dtype=int)
    tensor_word_intent = np.zeros([len_vocab, len(intent)], dtype=int)
    np.seterr(divide='ignore', invalid='ignore')
    ner_vocab = []
    ner_dict = {}
    for key, value in dataset.items():
        for data in value:
            token = tokenize(data)
            for i, t in enumerate(token):
                first_index = vocab.index(t)
                tensor_word_intent[first_index][intent.index(key)]+=1
                if len(token) > 1:
                    if i+1 < len(token):
                        if token[i+1][0]=="#":
                            ner_vocab.append(token[i+1])
                            if t in (ner_dict.keys()):
                                if token[i+1] in list(ner_dict[t].keys()):
                                    ner_dict[t][token[i+1]]+=1
                                else:
                                    ner_dict[t][token[i+1]]=1
                            else:
                                ner_dict[t]={token[i+1]: 1}
                        second_index = vocab.index(token[i+1])
                        tensor_word[first_index][second_index]+=1
            
    ner_vocab = list(sorted(set(ner_vocab)))
    ner_keys = list(sorted(ner_dict.keys()))
    tensor_ner = np.zeros([len(ner_keys), len(ner_vocab)], dtype=int)
    for key, value in ner_dict.items():
        key_index = ner_keys.index(key)
        for k, v in value.items():
            k_index = ner_vocab.index(k)
            tensor_ner[key_index][k_index] = v
    tensor_ner_ = (tensor_ner.T/tensor_ner.sum(axis=1)).T
    tensor_ner_ = np.nan_to_num(tensor_ner_)
    tensor_word_ = (tensor_word.T/tensor_word.sum(axis=1)).T
    tensor_word_ = np.nan_to_num(tensor_word_)
    tensor_word_intent_ = (tensor_word_intent.T/tensor_word_intent.sum(axis=1)).T
    tensor_word_intent_ = np.nan_to_num(tensor_word_intent_)
    pheremone = {
        "vocab": vocab,
        "tensor_word": tensor_word_.tolist(),
        "ner_keys": ner_keys,
        "tensor_word_intent": tensor_word_intent_.tolist(),
        "ner_dicts": ner_dicts,
        "tensor_ner": tensor_ner_.tolist()
    }
    pheremone = json.dumps(pheremone)
    print(pheremone)
    print(sys.getsizeof(pheremone))

mlTensor(tmp_dataset)
# def mlSupport(token):
#     #Skip-Fill Algo. Filling the skipped document.
#     if len(token)>2:
#         for i, t in enumerate(token):
#             t_index = token.index(t)
#             if (t_index+1)<len(token):
#                 if t in vocab and token[t_index+1] in vocab:
#                     if i==0:
#                         skip_value = list(tensor_word_[:,vocab.index(token[t_index])])
#                         if max(skip_value)>=0.6 and  skip_value.count(max(skip_value))==1:
#                             skip_index = skip_value.index(max(skip_value))
#                             token = [vocab[skip_index]] + token
#                             t_index = token.index(t)
#                     if tensor_word_[vocab.index(t)][vocab.index(token[t_index+1])]==0:
#                         fill_flag = True
#                         fill_value = 0.00
#                         skip_flag = True
#                         next_index = vocab.index(token[t_index+1])
#                         #get index of all non zero elements.
#                         fill_values = tensor_word_[vocab.index(token[t_index]),:]
#                         fill_indices = list(np.where(fill_values!=0)[0])
#                         fill_values = list(fill_values)
#                         for fill_index in fill_indices:
#                             if tensor_word_[fill_index][next_index]!=0:
#                                 if fill_value<tensor_word_[fill_index][next_index]:
#                                     fill_value=tensor_word_[fill_index][next_index]
#                                     token = token[:t_index+1]+[vocab[fill_index]]+token[t_index+1:]
#                                     fill_flag = False
#                         if fill_flag:
#                             if i!=0:
#                                 if token[t_index-1] in vocab:
#                                     if tensor_word_[vocab.index(token[t_index-1])][vocab.index(token[t_index+1])]!=0:
#                                         token = token[:t_index]+token[t_index+1:]
#                                     else:
#                                         break
#                 elif t not in ner_keys and t in vocab:
#                     fill_values = list(tensor_word_[vocab.index(token[t_index]),:])
#                     if fill_values.count(max(fill_values))==1:
#                         fill_index = fill_values.index(max(fill_values))
#                         token = token[:t_index+1]+[vocab[fill_index]]+token[t_index+1:]
#                     else:
#                         if token[t_index+1] not in vocab:
#                             fill_flag = True
#                             fill_values = tensor_word_[vocab.index(token[t_index]),:]
#                             fill_max = max(list(fill_values))
#                             fill_indices = list(np.where(fill_values==fill_max)[0])
#                             fill_values = list(fill_values)
#                             for fill_index in fill_indices:
#                                 if vocab[fill_index] in ner_keys and fill_flag:
#                                     token = token[:t_index+1]+[vocab[fill_index]]+token[t_index+1:]
#                                     fill_flag = False
#             else:
#                 if t in vocab:
#                     skip_value = list(tensor_word_[vocab.index(token[t_index]),:])
#                     if max(skip_value)>=0.6 and  skip_value.count(max(skip_value))==1:
#                         skip_index = skip_value.index(max(skip_value))
#                         token = token + [vocab[skip_index]]
#                         t_index = token.index(t)
#     return token

# def mlCore1(token):
#     intent_prediction = []
#     ner_word = []
#     ner_word_ = []
#     tmp_index = 0
#     for i, t in enumerate(token):
#         if t in vocab: # Check if 't' is present in Bot Vocab.
#             index = vocab.index(t)
#             # Predict the Intnent
#             if i==0:
#                 intent_prediction.append(list(tensor_word_intent_[index]))
#             else:
#                 if tensor_word_[vocab.index(token[i-1])][index]>0:
#                     intent_prediction.append(list(tensor_word_intent_[index]))
#                 else:
#                     break
#         else:
#             # Getting the Unknown Vocab ie. Named Entity
#             if i-tmp_index==1:
#                 ner_word.append(t)
#             else:
#                 if len(ner_word)>0:
#                     ner_word_.append(" ".join(ner_word))
#                     ner_word = []
#             if token[i-1] in ner_keys:
#                 ner_word.append(t)
#                 tmp_index = i
#     if len(ner_word) > 0:
#         ner_word_.append(" ".join(ner_word))

#     intent_prediction = np.array(intent_prediction)
#     intent_pre = list(intent_prediction.sum(axis=0))
#     max_val = max(intent_pre)
#     max_index = intent_pre.index(max_val)
#     if intent[max_index] in list(ner_dicts.keys()):
#         ner_type = ner_dicts[intent[max_index]]
#     else:
#         ner_type = ["Other"]
#     return ner_word_, intent[max_index], ner_type

# def mlCore2(token):
#     intent_prediction = []
#     ner_word = []
#     ner_word_ = []
#     tmp_index = 0
#     token_len = len(token)
#     for i, t in enumerate(token):
#         token_index = token.index(t)
#         if t in vocab:
#             index = vocab.index(t)
#         else:
#             index = None
#         if i+1<=token_len and token_len !=1:
#             if t in vocab and token[token_index+1] in vocab:
#                 next_index = vocab.index(token[token_index+1])
#                 if tensor_word_[index][next_index]>0:
#                     intent_prediction.append(list(tensor_word_intent_[index]))
#                 else:
#                     break
#             elif t in ner_keys:
#                 intent_prediction.append(list(tensor_word_intent_[index]))
#             else:
#                 # Getting the Unknown Vocab ie. Named Entity
#                 if token[token_index-1] in ner_keys:
#                     ner_word.append(t)
#                     tmp_index = token_index
#                 elif token_index-tmp_index<=1:
#                     ner_word.append(t)
#                     tmp_index = token_index
#                 else:
#                     if len(ner_word)>0:
#                         ner_word_.append(" ".join(ner_word))
#                         ner_word = []
#         else:
#             if index!=None:
#                 intent_prediction.append(list(tensor_word_intent_[index]))
            
#     if len(ner_word) > 0:
#         ner_word_.append(" ".join(ner_word))
    
#     intent_prediction = np.array(intent_prediction)
#     intent_pre = list(intent_prediction.sum(axis=0))
#     max_val = max(intent_pre)
#     max_index = intent_pre.index(max_val)
#     if intent[max_index] in list(ner_dicts.keys()):
#         ner_type = ner_dicts[intent[max_index]]
#     else:
#         if len(ner_word_)>0:
#             ner_type = ["Other"]
#         else:
#             ner_type = []
#     return ner_word_, intent[max_index], ner_type

# prePos = ['yours', 'your', 'their', 'he', 'she', 'him', 'her', 'his', 'they', 'them', 'our', 'it', 'which', 'that', 'its', 'this', 'those', 'there', 'these', 'here']
# def mlPre(context, token, ner_type):
#     mlNer = []
#     for t in token:
#         if len(mlNer)==len(ner_type):
#             break
#         if t in prePos:
#             for ner in ner_type:
#                 if len(context[ner])>0:
#                     mlNer += context[ner]
#     return mlNer

