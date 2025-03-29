import logging

import psycopg2
from db_models import User
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from utils import PasswordEngine

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    init_db = False
    with psycopg2.connect(
        database='messenger', user='postgres', password='postgres', host='postgres', port='5432'
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.users');")
            if cursor.fetchone()[0] is None:
                with open('init.sql', 'r', encoding='utf-8') as file:
                    cursor.execute(file.read())
                connection.commit()
                init_db = True
    if init_db:
        engine = create_engine(
            URL.create(
                drivername='postgresql',
                username='postgres',
                password='postgres',
                host='postgres',
                port='5432',
                database='messenger',
            )
        )
        with Session(engine) as session:
            session.add(
                User(login='admin', name='admin', surname='admin', password=PasswordEngine.hash_password('secret'))
            )
            for i in range(5):
                session.add(
                    User(
                        login=f'user{i}',
                        name=f'user{i}',
                        surname=f'user{i}',
                        password=PasswordEngine.hash_password('pass'),
                    )
                )
            session.commit()
