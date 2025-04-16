from flask import Flask, request, redirect, jsonify
import redis
import hashlib

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    short_key = hashlib.md5(long_url.encode()).hexdigest()[:6]
    r.set(short_key, long_url)
    return jsonify({'short_url': request.host_url + short_key})

@app.route('/<short_key>', methods=['GET'])
def redirect_url(short_key):
    long_url = r.get(short_key)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

