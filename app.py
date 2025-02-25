from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS for development
import sqlite3  # Use SQLite for simplicity in POC

app = Flask(__name__)
CORS(app)  # Enable CORS

DATABASE = 'events.db'  # SQLite database file

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# API endpoint to receive events
@app.route('/api/events', methods=['POST'])
def track_event():
    if request.headers.get('x-api-key')!= 'YOUR_API_KEY':  # API key validation
        return jsonify({'error': 'Unauthorized'}), 401

    event_data = request.get_json()
    # Store event data in database
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                eventType TEXT NOT NULL,
                eventData TEXT,
                timestamp INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO events (userId, eventType, eventData, timestamp)
            VALUES (?,?,?,?)
        ''', (event_data['userId'], event_data['eventType'],
              json.dumps(event_data['eventData']), event_data['timestamp']))
        db.commit()
        return jsonify({'message': 'Event tracked'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
