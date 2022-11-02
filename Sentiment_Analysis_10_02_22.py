# import sys
# from transformers import pipeline
#
# nlp = pipeline(task = 'sentiment-analysis',
#                model = 'nlptown/bert-base-multilingual-uncased-sentiment')
#
# # text = ['its a good day']
#
# text = input('Type sentence: ')
# text = [text]
# # print(type(text))
# # text = list(text)
# # print(len(text))
# print(text)
# # print(f'{nlp(text)}')
#
# result = nlp(text)
# sent = ''
#
# def sentiment_provider(text):
#     for i in range(len(text)):
#         if (result[i]['label'] == '1 star'):
#             sent = 'very negative'
#         elif (result[i]['label'] == '2 star'):
#             sent = 'negative'
#         elif (result[i]['label'] == '3 stars'):
#             sent = 'neutral'
#         elif (result[i]['label'] == '4 stars'):
#             sent = 'positive'
#         else:
#             sent = 'very positive'
#
#         print('Text is: ' + str(text[i]))
#         print('sentiment: ' + str(sent) + ' & ' + 'probability: ' + str(result[i]['score']))
#
#
# sentiment_provider(text)


import sys
from transformers import pipeline

nlp = pipeline(task = 'sentiment-analysis',
               model = 'nlptown/bert-base-multilingual-uncased-sentiment')

def sentiment_provider():
    text = input('Type sentence: ')
    text = [text];
    print(text)

    result = nlp(text)
    sent = ''

    for i in range(len(text)):
        if (result[i]['label'] == '1 star'):
            sent = 'very negative'
        elif (result[i]['label'] == '2 star'):
            sent = 'negative'
        elif (result[i]['label'] == '3 stars'):
            sent = 'neutral'
        elif (result[i]['label'] == '4 stars'):
            sent = 'positive'
        else:
            sent = 'very positive'

        print('Text is: ' + str(text[i]))
        print('sentiment: ' + str(sent) + ' & ' + 'probability: ' + str(result[i]['score']))


sentiment_provider()
