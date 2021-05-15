from my_app import app, db, cache
from flask import jsonify, request, make_response
from ..models.company import Company
import uuid


@app.route('/company/create', methods=['POST'])
@cache.cached(timeout=50)
def create_shop():
    id = uuid.uuid4()
    company = Company(
        id=id,
        name=request.json['name'],
        password=request.json['password'],
    )
    db.session.add(company)
    db.session.commit()
    company = Company.load_company(id)
    return make_response(jsonify(company), 201)
