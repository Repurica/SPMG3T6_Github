from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# importing and registering the blueprint
# test this endpoint at 
# http://127.0.0.1:5000/sample/all_employee 
# http://127.0.0.1:5000/sample/one_employee?id=140001 
from sample import sample
app.register_blueprint(sample, url_prefix="/sample")

from schedule import schedule
app.register_blueprint(schedule, url_prefix="/schedule")

from application import application
app.register_blueprint(application, url_prefix='/application')

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, Route: {rule}")
@app.route('/')
def home():
    return "running!!"

if __name__ == '__main__':
    app.run(debug=True)
