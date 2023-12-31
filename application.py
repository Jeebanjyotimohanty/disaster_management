import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Initialize the MongoDB client and connect to your MongoDB Atlas cluster
client = MongoClient("mongodb+srv://jeebanjyoti2003:jeeban@cluster0.x2c1ueu.mongodb.net/")
db = client["your_database_name"]  # Replace "your_database_name" with your actual database name

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/commonalerts", methods=["GET", "POST"])
def commonalerts():
    if request.method == "POST":
        c = request.form.get("calamity")
        l = request.form.get("location")
        d = request.form.get("description")
        
        # Access the collection in MongoDB
        commonalerts_collection = db["commonalerts"]
        
        # Insert the document into MongoDB
        commonalerts_collection.insert_one({
            "calamity": c,
            "location": l,
            "description": d
        })
        
        return "Alert Issued Successfully.", 200
    else:
        return render_template("alerts.html")

@app.route("/getcommonalerts")
def getcommonalerts():
    alerts = []
    
    # Access the collection in MongoDB
    commonalerts_collection = db["commonalerts"]
    
    # Query all documents from MongoDB
    common_alerts = commonalerts_collection.find().sort("datetime", -1)
    
    for alert in common_alerts:
        s = {
            "datetime": alert.get("datetime"),
            "location": alert.get("location"),
            "calamity": alert.get("calamity"),
            "description": alert.get("description")
        }
        alerts.append(s)
    
    return jsonify(alerts)

@app.route("/govtalerts", methods=["GET", "POST"])
def govtalerts():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Access the collection in MongoDB for user authentication
        govtids_collection = db["govtids"]
        user = govtids_collection.find_one({"username": username})
        
        if user is None or not user["password"] == password:
            return "Invalid username and/or password"
        
        c = request.form.get("calamity")
        l = request.form.get("location")
        d = request.form.get("description")
        
        # Access the collection in MongoDB for government alerts
        govtalerts_collection = db["govtalerts"]
        
        # Insert the document into MongoDB
        govtalerts_collection.insert_one({
            "calamity": c,
            "location": l,
            "description": d
        })
        
        return "Alert Issued Successfully.", 200
    else:
        return render_template("govtalerts.html")

@app.route("/getgovtalerts")
def getgovtalerts():
    alerts = []
    
    # Access the collection in MongoDB
    govtalerts_collection = db["govtalerts"]
    
    # Query all documents from MongoDB
    govt_alerts = govtalerts_collection.find().sort("datetime", -1)
    
    for alert in govt_alerts:
        s = {
            "datetime": alert.get("datetime"),
            "location": alert.get("location"),
            "calamity": alert.get("calamity"),
            "description": alert.get("description")
        }
        alerts.append(s)
    
    return jsonify(alerts)

@app.route("/collaboration", methods=["GET", "POST"])
def collaboration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        team_id = request.form.get("team_id")
        calamity = request.form.get("calamity")
        location = request.form.get("location")
        reason = request.form.get("reason")
        
        # Access the collection in MongoDB for user authentication
        rescueteamids_collection = db["rescueteamids"]
        user = rescueteamids_collection.find_one({"username": username})
        
        if user is None or not user["password"] == password:
            return "Invalid username and/or password"
        
        # Access the collection in MongoDB for collaboration alerts
        collaboration_collection = db["collaboration"]
        
        # Insert the document into MongoDB
        collaboration_collection.insert_one({
            "team_id": team_id,
            "calamity": calamity,
            "location": location,
            "reason": reason
        })
        
        return "Alert Issued Successfully.", 200
    else:
        return render_template("collaboration.html")

@app.route("/getcollaborationalerts")
def getcollaborationalerts():
    alerts = []
    
    # Access the collection in MongoDB for collaboration alerts
    collaboration_collection = db["collaboration"]
    
    # Query all documents from MongoDB
    collaboration_alerts = collaboration_collection.find().sort("datetime", -1)
    
    for alert in collaboration_alerts:
        s = {
            "team_id": alert.get("team_id"),
            "datetime": alert.get("datetime"),
            "calamity": alert.get("calamity"),
            "location": alert.get("location"),
            "reason": alert.get("reason")
        }
        alerts.append(s)
    
    return jsonify(alerts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)