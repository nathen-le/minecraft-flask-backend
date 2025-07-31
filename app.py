import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from mcstatus import JavaServer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/query', methods=['GET'])
def query_server():
    address = request.args.get('address')
    port = request.args.get('port', default=25565, type=int)
    if not address:
        return jsonify({"error": "Missing server address"}), 400

    try:
        server = JavaServer.lookup(f"{address}:{port}")
        status = server.status()
        player_names = [p.name for p in status.players.sample] if status.players.sample else []
        response = {
            "players_online": status.players.online,
            "players_max": status.players.max,
            "latency_ms": status.latency,
            "version": status.version.name,
            "motd": status.description,
            "player_names": player_names
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Minecraft Server Stats API is running."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
