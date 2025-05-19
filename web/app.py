from flask import Flask, request, jsonify, render_template
import mysql.connector

import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

def insert_ip(ip):
    try:
        logger.info(f"Connecting using config: {MYSQL_CONFIG}")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ip_logs (ip_address) VALUES (%s)", (ip,))
        conn.commit()
        return jsonify({'message': f'IP {ip} logged successfully'}), 200
    except mysql.connector.Error as err:
        logger.error(err)
            # Any other database error
        raise jsonify({
            'status': 'error',
            'message': str(err)
        })

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

@app.route('/log-ip', methods=['POST'])
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    try:
        insert_ip(ip)
        return jsonify({'status': 'success', 'ip_logged': ip}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ip_logs")
        rows = cursor.fetchall()
        return render_template('index.html', ip_logs=rows)
    except mysql.connector.Error as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
