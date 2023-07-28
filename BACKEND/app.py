from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from mangum import Mangum
from waitress import serve


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb+srv://hiruvidu586:Hirushan2588071M@cluster0.4oftrlo.mongodb.net/test_db?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)
db = mongodb_client.db

handler = Mangum(app)

@app.route('/users', methods=['GET','POST'])
def add_user():
    if request.method == 'GET':
        users = db.demcareusers.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return jsonify({'users': user_list})

    elif request.method == 'POST':
        data = request.get_json()
        caregiverusername = data.get('caregiverusername')
        caregiverfristname = data.get('caregiverfristname')
        caregiverlastname = data.get('caregiverlastname')
        caregivergender = data.get('caregivergender')
        caregiverage = data.get('caregiverage')
        patientusername = data.get('patientusername')
        patientfristname = data.get('patientfristname')
        patientlastname = data.get('patientlastname')
        patientgender = data.get('patientgender')
        patientage = data.get('patientage')
        password = data.get('password')
        email = data.get('email')
        telephone = data.get('telephone')

        if not caregiverusername or not caregiverfristname or not caregiverlastname or not caregivergender or not caregiverage or not patientusername or not patientfristname or not patientlastname or not patientgender or not patientage or not password or not email or not telephone:
            return jsonify({'message': 'All the data must be filled'}), 400
        
        existing_caregiver = db.users.find_one({'caregiverusername': caregiverusername})
        if existing_caregiver:
            return jsonify({'message': 'Caregiver username already exists'}), 400
        
        existing_patient = db.users.find_one({'patientusername': patientusername})
        if existing_patient:
            return jsonify({'message': 'Patient username already exists'}), 400

        user = {
            'caregiverusername': caregiverusername,
            'caregiverfristname' : caregiverfristname,
            'caregiverlastname' : caregiverlastname,
            'caregivergender': caregivergender,
            'caregiverage' : caregiverage,
            'patientusername' : patientusername,
            'patientfristname' : patientfristname,
            'patientlastname' : patientlastname,
            'patientgender' : patientgender,
            'patientage' : patientage,
            'password' : password,
            'email' : email,
            'telephone' : telephone
    
            
        }

        result = db.demcareusers.insert_one(user)

        return jsonify({'message': 'User added successfully', 'user_id': str(result.inserted_id)})

@app.route('/caregiver/<caregiverusername>', methods=['GET'])
def get_caregiver(caregiverusername):
    
    user = db.demcareusers.find_one({'caregiverusername': caregiverusername})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user['_id'] = str(user['_id'])

    return jsonify({'user': user})

@app.route('/patient/<patientusername>', methods=['GET'])
def get_patient(patientusername):

    user = db.demcareusers.find_one({'patientusername': patientusername})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user['_id'] = str(user['_id'])

    return jsonify({'user': user})

@app.route('/logincaregiver', methods=['POST'])
def logincaregiver():
    data = request.get_json()
    caregiverusername = data.get('caregiverusername')
    patientusername = data.get('patientusername')
    password = data.get('password')

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    if not caregiverusername or not patientusername:
        return jsonify({'message': 'Both caregiver and patient usernames are required'}), 400

    caregiver_user = db.demcareusers.find_one({'caregiverusername': caregiverusername})
    if caregiver_user and caregiver_user['password'] == password:

        patient_user = db.demcareusers.find_one({'patientusername': patientusername, 'password': password})
        if patient_user:
            return jsonify({'message': 'Login successful', 'user_id': str(patient_user['_id'])})
        else:
            return jsonify({'message': 'Invalid patient username or password'}), 401

    return jsonify({'message': 'Invalid caregiver username or password'}), 401



@app.route('/loginpatient', methods=['POST'])
def loginpatient():
    data = request.get_json()
    patientusername = data.get('patientusername')
    password = data.get('password')

    if not patientusername or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = db.demcareusers.find_one({'patientusername': patientusername})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user['password'] != password:
        return jsonify({'message': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])})
    


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)




