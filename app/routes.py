from flask import Flask, request, jsonify
from app.models import db, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/api/notes', methods=['GET'])
def get_notes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search_query = request.args.get('search', '', type=str)

    query = Note.query
    if search_query:
        query = query.filter(Note.title.contains(search_query))

    paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "notes": [{"id": n.id, "title": n.title, "content": n.content} for n in paginated_data.items],
        "total_pages": paginated_data.pages,
        "current_page": paginated_data.page
    }), 200


@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Bad Request. Missing fields"}), 400

    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "message": "Note created successfully"}), 201


if __name__ == '__main__':
    # База данных для обычной работы создается только при прямом запуске сервера
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)


