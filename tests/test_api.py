import pytest
from app.routes import app, db
from app.models import Note  # Явно импортируем модели, чтобы они зарегистрировались в метаданных


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Гарантированно очищаем старые следы
            db.create_all()  # Создаем чистые таблицы с актуальными колонками
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_empty_db(client):
    response = client.get('/api/notes')
    assert response.status_code == 200
    assert len(response.get_json()['notes']) == 0

