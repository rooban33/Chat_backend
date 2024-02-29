from requests.exceptions import ConnectionError
from custom import Custom
from flask import Flask, request
from flask_cors import CORS

# ------------------ SETUP ------------------


app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)

# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500

# ------------------ CUSTOM API ------------------

custom = Custom()

@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    print(body)
    if body['messages'][0]['text'] == 'chart':
            return {"html": "<div>\
  <div style=\"margin-bottom: 10px\">Here is an example chart:</div>\
  <google-chart\
    style=\"width: 220px; height: 200px\"\
    data='[\"Planet\", \"Score\"], [\"Earth\", 50], [\"Moon\", 100], [\"Saturn\", 80]'\
    options='{\"legend\": \"none\"}'>\
  </google-chart>\
</div>"}
    if body['messages'][0]['text'] == 'table':
         return {'html': '<div><h2>Simple Table</h2><table border=1><thead><tr><th>ID</th><th>Name</th><th>Age</th><th>Email</th></tr></thead><tbody><tr><td>1</td><td>John Doe</td><td>30</td><td>john@example.com</td></tr><tr><td>2</td><td>Jane Smith</td><td>25</td><td>jane@example.com</td></tr><tr><td>3</td><td>Michael Johnson</td><td>35</td><td>michael@example.com</td></tr></tbody></table></div>' 
  }
    if body['messages'][0]['text'] == 'image':
         return {'html':'<img src="glow.gif" height="90" width="80" />' }

    return {"text": "Hello"}

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)

@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)
@app.route("/", methods=["POST"])
def default():
    print("Im working")

# ------------------ START SERVER ------------------

if __name__ == "__main__":
    app.run(port=8080)