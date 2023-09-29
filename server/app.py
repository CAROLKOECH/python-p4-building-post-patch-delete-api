from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# Create a new review
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json

    if not all(key in data for key in ('score', 'comment', 'user_id', 'game_id')):
        return jsonify({'error': 'Missing data fields'}), 400

    new_review = Review(
        score=data['score'],
        comment=data['comment'],
        user_id=data['user_id'],
        game_id=data['game_id']
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify(new_review.to_dict()), 201

# Read all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = [review.to_dict() for review in Review.query.all()]
    return jsonify(reviews), 200

# Read a specific review by ID
@app.route('/reviews/<int:id>', methods=['GET'])
def get_review_by_id(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.to_dict()), 200

# Update a specific review by ID
@app.route('/reviews/<int:id>', methods=['PATCH'])
def update_review(id):
    data = request.json

    if not all(key in data for key in ('score', 'comment')):
        return jsonify({'error': 'Missing data fields'}), 400

    review = Review.query.get(id)

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    review.score = data['score']
    review.comment = data['comment']

    db.session.commit()

    return jsonify(review.to_dict()), 200

# Delete a specific review by ID
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
