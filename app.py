from flask import Flask, request, jsonify, send_from_directory
from mcstatus import JavaServer

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    # Serve the frontend HTML page
    return send_from_directory('.', 'index.html')

@app.route('/query', methods=['GET'])
def query_server():
    address = request.args.get('address')
    port = request.args.get('port', default=25565, type=int)
    if not address:
        return jsonify({"error": "Missing server address"}), 400

    try:
        server = JavaServer.lookup(f"{address}:{port}")
        status = server.status()
        # Extract player names if available
        player_names = []
        if status.players.sample:
            player_names = [player.name for player in status.players.sample]

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

if __name__ == '__main__':
    app.run(debug=True)
