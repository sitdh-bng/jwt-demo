import os
import jwt

from flask import Flask, g, jsonify, make_response, request

app = Flask(__name__)

UNAUTHORIZED_CODE = 401
SUCCESS_WITH_UPDATE = 201

@app.route('/')
def home():
    return make_response(
        jsonify({
            'ping': 'pong',
        }),
        201
    )

@app.route('/returngoods', methods=['POST'])
def return_goods():
    payload = {}

    response_code = UNAUTHORIZED_CODE
    response_message = {
        'response': 'Failure',
        'reason': 'Unauthorizaed'
    }

    try:
        token = request.headers.get('Authorization').split(' ').pop()
        
        payload = jwt.decode(
            token, 
            os.environ.get('SECRET_KEY', 'super-secret-token'),
            algorithms=['HS256']
        )
        
        response_code, response_message, is_all_mandatory_request_fields_exists = field_validation(
            request.json, 
            ['doc_no', 'refer_doc_no', 'request_type',]
        )
        _, _, is_all_mandatory_payload_fields_exists = field_validation(
            payload, 
            ['iss', 'sub', 'aud', 'iat', 'exp',]
        )
        
        if (is_all_mandatory_fields_exists and is_all_mandatory_payload_fields_exists) \
            and 'Arokaya Labs' != payload.get('iss', 'Arokaya Labs'):
            
            response_message['response'] = 'Success'
            response_message['reason'] = 'Action complete'
            response_code = SUCCESS_WITH_UPDATE
            
    except:
        pass

    return make_response(
        jsonify(response_message),
        response_code
    )

def field_validation(doc, fields):
    fields_compare = set(
        # Mandatory fields
        fields
    ).difference(set(doc.keys()))

    response_message = {
        'response': 'Success',
        'reason': 'Action complete'
    }
    response_code = SUCCESS_WITH_UPDATE
    
    MESSAGE_VALID = True

    if bool(fields_compare):
        response_message = {
            'response': 'Failure',
            'reason': 'Invalid format'
        }
        response_code = UNAUTHORIZED_CODE
        MESSAGE_VALID = False

    return response_code, response_message, MESSAGE_VALID

@app.route('/api/v0/secret-key', methods=['GET'])
def get_secret_keys():
    return make_response(
        jsonify({
            'key': os.environ.get('SECRET_KEY')
        }),
        SUCCESS_WITH_UPDATE
    )
