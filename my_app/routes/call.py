from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.call import Call
from ..utils.errors import ClientError
import uuid


@app.route('/calls/new-call', methods=['POST'])
def create_call():
    id = uuid.uuid4()
    call = Call (
        id=id,
        employeeId=request.json['employeeId'],
        shopId=request.json['shopId'],
        rating=request.json['rating'],
        date=request.json['date']
    )
    db.session.add(call)
    db.session.commit()
    call = Call.load_call(str(id))
    return make_response(jsonify(call), 201)

@app.route('/calls/<callId>', methods=['PUT'])
def add_call_rating(callId):
    call = Call.query.get(callId)

    if request.json['rating']:   call.rating =  request.json['rating']
    
    db.session.commit()

    return make_response(jsonify(call.serialize()), 200)