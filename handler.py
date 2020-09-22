import json
from spell_checker import spell_check_sentence
from similarities import search_similarities
from db import DBStorage

def spell_check(event, context):
    request = (json.loads(event['body']))['text']
    result = spell_check_sentence(request)
    body = {
        "text": result
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    dbstorage = DBStorage()
    dbstorage.save_history(request = request, result= result)
    return response
    
def similarity(event, context):
    request = (json.loads(event['body']))
    result = search_similarities(request['options'], request['text'])
    body = result
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
