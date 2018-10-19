from flask import Flask, render_template, request, jsonify
import json
import eq_debugger
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("main.html", title="Math Debugger")

@app.route("/echo", methods=['POST'])
def webhook():
    print(request.headers)
    print("body: {0}".format(request.data))
    return request.data

@app.route('/postText', methods=['POST'])
def lower_conversion():
   text = request.json['text']
   if "ping" in text:
       return_data = {"result":"pong"}
       return jsonify(ResultSet=json.dumps(return_data))
   #lower_text = text.lower()
   #return_data = {"result":lower_text}
   debug_text = eq_debugger.check_total_answer(text)
   return_data = {"result": debug_text}
   return jsonify(ResultSet=json.dumps(return_data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
