from random import randint, choice
from faker import Faker
from app import app, db, User, Game, Review  # Import the 'app' variable

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    for _ in range(100):
        user = User(name=fake.name())
        users.append(user)

    db.session.add_all(users)

    games = []
    for _ in range(100):
        game = Game(
            title=fake.sentence(),
            genre=choice(["Action", "Adventure", "RPG", "Simulation"]),
            platform=choice(["PC", "PlayStation", "Xbox", "Nintendo"]),
            price=randint(10, 60)
        )
        games.append(game)

    db.session.add_all(games)

    reviews = []
    for user in users:
        for _ in range(randint(1, 5)):
            review = Review(
                score=randint(1, 10),
                comment=fake.text(max_nb_chars=200),
                user=user,
                game=choice(games)
            )
            reviews.append(review)

    db.session.add_all(reviews)

    db.session.commit()
