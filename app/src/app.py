from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email FROM users')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'username': row[1],
            'email': row[2]
        })

    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id',
        (username, email, password)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'id': new_id,
        'username': username,
        'email': email
    }), 201

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)