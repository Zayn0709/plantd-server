from flask import Flask, request
from db import db
from bson.objectid import ObjectId
from PIL import Image

import os
import detection



app = Flask(__name__, static_url_path='/public', static_folder='assets')



@app.route('/detect', methods=['POST'])
def detect():
    img = request.files.get('file')
    img = Image.open(img)
    result = detection.detect(img)
    dis = db['disease']
    res = dis.find_one({
        'key': result['predict_name']
    })
    res['_id'] = str(res['_id'])
    res['plantId'] = str(res['plantId'])
    return res


@app.route('/plants', methods=['GET'])
def plants():
    plant = db['plant']
    result = plant.aggregate([
        {
            '$lookup': {
                'from': 'disease',
                'localField': '_id',
                'foreignField': 'plantId',
                'as': 'diseases'
            }
        },{
            '$project': {
                '_id': 1,
                'name': 1,
                'imgUrl': 1,
                'diseases_count': {
                    '$size': '$diseases'
                }
            }
        }
    ])
    data = []
    for item in result:
        item['_id'] = str(item['_id'])
        data.append(item)

    return {
        'data': data
    }


@app.route('/tomatodiseases', methods=["GET"])
def tomatoDiseases():
    disease = db['disease']
    plantId = '5dd6c573aa3cd5187425eedf'
    result = disease.aggregate([
        {
            '$match': {
                'plantId': ObjectId(plantId)
            }
        },{
            '$project': {
                'cause_type': 1,
                'disease': 1,
                'imgUrl': 1,
                '_id': 1
            }
        }
    ])

    data = []
    for item in result:
        item['_id'] = str(item['_id'])
        data.append(item)
    
    return {
        'data': data
    }

@app.route('/diseases', methods=["GET"])
def diseases():
    disease = db['disease']
    result = disease.aggregate([
        {
            '$match': {
                'plantId': ObjectId(request.args.get('plantid'))
            }
        },{
            '$project': {
                'cause_type': 1,
                'disease': 1,
                'imgUrl': 1,
                '_id': 1
            }
        }
    ])

    data = []
    for item in result:
        item['_id'] = str(item['_id'])
        data.append(item)
    
    return {
        'data': data
    }


@app.route('/disease', methods=['GET'])
def disease():
    diasese = db['disease']
    result = diasese.find_one({
        '_id': ObjectId(request.args.get('id'))
    })
    result['_id'] = str(result['_id'])
    result['plantId'] = str(result['plantId'])
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
