#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from datetime import datetime, timedelta

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for _ in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    """Deletes old messages and generates 20 new random messages."""

    with app.app_context():
        # Clear existing messages and commit to reset DB state
        Message.query.delete()
        db.session.commit()

        messages = []

        for _ in range(20):
            created_at = fake.date_time_between(start_date="-30d", end_date="now")  # Random past dates
            message = Message(
                body=fake.sentence(),
                username=rc(usernames),
                created_at=created_at,
                updated_at=created_at  # Set updated_at to match initially
            )
            messages.append(message)

        db.session.add_all(messages)
        db.session.commit()

        print("Database successfully seeded with messages!")

if __name__ == '__main__':
    make_messages()
