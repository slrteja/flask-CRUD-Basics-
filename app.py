from flask import Flask, flash, jsonify,render_template,request,url_for,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from sqlalchemy import true

app = Flask(__name__)
app.secret_key = "8756aefasaf1e567huhgybhjbuy8945"

client = MongoClient('localhost', 27017)

db = client.company
details = db.details

# ...

@app.route('/', methods=('GET','POST','PUT'))
def index():
    print(request.form)
    if request.method=='POST':
            user={
            "name" : request.form.get('name'),
            "gender" : request.form.get('gender'),
            "email": request.form.get('email'),
        }
            if db.details.find_one({"email": user["email"]}):
                db.details.update_one({"email": "email"},{"$set": {"name": "name", "email": "email","gender": "gender"}},upsert=True)
                return jsonify("error Email already exists")
            elif db.details.insert_one(user):
                flash('Thanks for adding this information')
            return redirect(url_for('index'))
    all_details = details.find()
    return render_template('index.html', details=all_details)
    
        
# ...

@app.post('/<id>/delete/')
def delete(id):
    details.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# ...

#...

@app.route('/update/',methods=['POST','GET'])
def edit():
    print (request.form)
    name=request.form.get('name')
    email=request.form.get('email')
    gender=request.form.get('gender')
    details.update_one({"email": email},{"$set": {"name": name ,"gender": gender}})
    return render_template('edit.html')


if __name__ == "__main__":
    app.run(debug=true)