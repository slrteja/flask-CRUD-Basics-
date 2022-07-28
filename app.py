from distutils.log import error
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
            "category" : request.form.get('category'),
            "email": request.form.get('email'),
            "number" : request.form.get('number'),
        }
            if db.details.find_one({"email": user["email"]}) or db.details.find_one({"number": user["number"]}):
                error("already user created with email")
                return jsonify({"error" : "Email already exists"})
            elif db.details.insert_one(user):
                details.create_index("email")
                flash('Thanks for adding this information')
            return redirect(url_for('index'))
    all_details = details.find()
    return render_template('index.html', details=all_details,)
def searchdata():
    if request.method=='POST':
        search=request.form.get('search')
        search_details=details.find_one({"name": search})
        return render_template('search.html',details=search_details)
    
    
        
# ...

@app.post('/<id>/delete/')
def delete(id):
    details.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# ...

@app.route('/edit/')
def edit_page():
    return render_template('edit.html')

#...

@app.route('/update/',methods=['POST','GET'])
def edit():
    print (request.form)
    name=request.form.get('name')
    email=request.form.get('email')
    category=request.form.get('category')
    number=request.form.get('number')
    if details.find_one_and_update({"email": email},{"$set": {"name": name ,"category": category,"number": number}}):
        return redirect(url_for('index'))
    elif jsonify("Data does not exists"):
        return render_template('edit.html')
    return render_template('edit.html')
    

@app.route('/delete/page/',methods=['POST','DELETE'])
def dpage():
    print (request.form)
    email=request.form.get('email')
    number=request.form.get('number')
    if db.details.find_one_and_delete({"email": email}) or db.details.find_one_and_delete({"number": number}):
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/delete/')
def delete_page():
    details.f
    return render_template('delete.html')

@app.route('/search/', methods=['GET'])
def search():
    key=request.values.get('key')
    refer=request.values.get('refer')
    if (key=="_id"):
        search_details=db.details.find({refer:ObjectId(key)})
    else:
        #search_details=db.details.find({refer:key})
        search_details=db.details.find({refer:key})
        #return jsonify("Details not found")
    return render_template('search.html', results=search_details)

@app.post('/file/')
def file():
    file=request.files['file']
    string=file.read().decode("utf-8")
    text={"filename":file.filename, "name":string}
    db.details.insert_one(text)

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=true)