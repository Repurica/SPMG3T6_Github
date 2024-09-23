from flask import Flask
app = Flask(__name__)






# importing and registering the blueprint
# test this endpoint at 
# http://127.0.0.1:5000/sample/all_employee 
# http://127.0.0.1:5000/sample/one_employee?id=140001 
from sample import sample
app.register_blueprint(sample, url_prefix="/sample")




@app.route('/')
def home():
    return "running!!"

if __name__ == '__main__':

    app.run(debug=True)
    
    
