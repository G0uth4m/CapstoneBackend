from flask import request, Response, jsonify
from app import app, mongo

@app.route('/api/v1/ip/url', methods=["POST"])
def send_url():
    if not request.json or not request.json.get("url"):
        return Response(status=400)
    
    url = request.json.get("url")
    ip = request.remote_addr

    collection = mongo.db.ips
    if collection.find_one({'ip': ip}):
        collection.update_one({'ip': ip}, {'$addToSet': {'urls': url}})
    else:
        collection.insert_one({'ip': ip, 'urls': [url]})
    
    return Response(status=200)

@app.route('/api/v1/ip', methods=["GET"])
def list_ips():
    collection = mongo.db.ips
    res = list(collection.find({}, {'_id': 0}))

    if not res:
        return Response(status=204)
    
    return jsonify(res)

@app.route('/api/v1/db/clear', methods=["DELETE"])
def clear_db():
    collection = mongo.db.ips
    res = collection.remove({})
    if res['n'] == 0:
        return Response(status=400)
    
    return Response(status=200)