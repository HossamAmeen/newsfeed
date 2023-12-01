from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'database': 'newsfeed',
    'user': 'root',
    'password': 'root'
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print(f"Connected to MySQL Server: {connection.get_server_info()}")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/posts/', methods=['POST'])
def add_post():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            data = request.json
            query = "INSERT INTO post (content, user_id) VALUES (%s, %s)"
            values = (data['content'], data['user_id'])
            cursor.execute(query, values)
            connection.commit()
            return jsonify({'message': 'post added successfully'}), 201
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            connection.close()


@app.route('/posts/<int:post_id>/', methods=['PUT'])
def update_post(post_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            data = request.json
            query = "UPDATE post SET Content = %s WHERE id = %s"
            values = (data['content'], post_id)
            cursor.execute(query, values)
            connection.commit()
            return jsonify({'message': 'post updated successfully'}), 200
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            connection.close()

@app.route('/posts/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM post WHERE id = %s"
            cursor.execute(query, (post_id,))
            connection.commit()
            return jsonify({'message': 'post deleted successfully'}), 200
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            connection.close()

@app.route('/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM post WHERE id = %s"
            cursor.execute(query, (post_id,))
            post = cursor.fetchone()
            if post:
                return jsonify(post), 200
            else:
                return jsonify({'error': 'post not found'}), 404
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run()
