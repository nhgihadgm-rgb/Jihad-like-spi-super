from flask import Flask, jsonify, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEYS = ["MR19"]

@app.route("/")
def home():

    return jsonify({

        "status": "online",

        "developer": "Jihad X Codex"

    })

@app.route("/like")
def like():

    uid = request.args.get("uid")

    server = request.args.get("server_name", "bd")

    key = request.args.get("key")

    # API KEY CHECK

    if key not in API_KEYS:

        return jsonify({

            "status": "error",

            "message": "Invalid API Key"

        })

    # UID CHECK

    if not uid:

        return jsonify({

            "status": "error",

            "message": "UID Missing"

        })

    try:

        # ORIGINAL API

        api = f"https://silent-vip-like-api.up.railway.app//like?uid={uid}&server_name={server}&key=MR19"

        response = requests.get(api, timeout=10)

        data = response.json()

        # PLAYER DATA

        player_name = data.get("PlayerNickname", "UNKNOWN")

        before_like = int(data.get("LikesbeforeCommand", 0))

        api_like = int(data.get("LikesGivenByAPI", 0))

        # EXTRA LIKE

        extra_like = 100

        # TOTAL LIKE

        total_like_added = api_like + extra_like

        # AFTER LIKE

        after_like = before_like + total_like_added

        # FINAL RESPONSE

        return jsonify({

            "player_name": player_name,

            "uid": uid,

            "before_like": before_like,

            "like_added": total_like_added,

            "after_like": after_like,

            "server": server.upper(),

            "status": "success",

            "developer": "Jihad X Codex",

            "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(

        host="0.0.0.0",

        port=port

    )