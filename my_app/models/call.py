from my_app import db


class Call(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    employeeId = db.Column(db.String(150), nullable=False)
    shopId = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "employeeId": self.employeeId,
            "shopId": self.shopId,
            "rating": self.rating,
            "date": self.date
        }
    @staticmethod
    def load_call(call_id):
        return Call.query.get(str(call_id)).serialize()

    def __repr__(self):
        return f"Call('{self.id}', '{self.employeeId}', '{self.rating}')"


db.create_all()
