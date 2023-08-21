from flask import Flask, jsonify, request
import numpy as np
import folium
import pandas as pd
from flask_pymongo import PyMongo
from mangum import Mangum
from waitress import serve
import requests


app = Flask(__name__)

handler = Mangum(app)

app.config["MONGO_URI"] = "mongodb+srv://hiruvidu586:Hirushan2588071M@cluster0.4oftrlo.mongodb.net/test_db?retryWrites=true&w=majority"


# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route('/lastrecode', methods=['GET'])
def handle_api():
        last_record = db.routesflask.find_one(sort=[('_id', -1)])

        if last_record:
            # Convert the record's _id to a string
            last_record['_id'] = str(last_record['_id'])
            
            # Return the last record as a JSON response
            return jsonify({'routesflask': last_record})

        # Return an appropriate response if there are no records
        return jsonify({'message': 'No records found'})


@app.route('/api', methods=['POST'])
def run_algorithm():
    # Get request parameters
    data = request.get_json()
    start_lat = data.get('StartLat')
    start_lon = data.get('StartLon')
    end_lat = data.get('EndLat')
    end_lon = data.get('EndLon')
    temple = data.get('Temples')
    heritages = data.get('Heritages')
    beaches = data.get('Beaches')
    parks = data.get('Parks')
    arts = data.get('Arts')
    username = data.get('Username')

    # Call main function
    result = main(start_lat, start_lon, end_lat, end_lon, temple, heritages, beaches, parks, arts)

    routeww = {
        'userName': username,
        'result': result
    }

    # Save result to MongoDB
    db.routesflask.insert_one(routeww)

    return 'Success'

def main(StartLat, StartLon, EndLat, EndLon, Temples, Heritages, Beaches, Parks, Arts):
    # print(StartLat)
    # print(StartLon)
    # print(EndLat)
    # print(EndLon)
    # print(Temples)
    # print(Heritages)
    # print(Beaches)
    matrixTemple = np.zeros((1, 2))
    rowsTemple = ['Avarage Distance']
    columnsTemple = ['Japanese Peace Pagoda', 'Shri Sudharmalaya Buddhist Temple\t']
    df1 = pd.DataFrame(matrixTemple, index=rowsTemple, columns=columnsTemple)
    
    matrixHeritageAndHistoricalPlaces = np.zeros((1, 7))
    rowsHeritagesHeritageAndHistoricalPlaces = ['Avarage Distance']
    columnsHeritageHeritageAndHistoricalPlaces = ['Galle Fort', 'Galle Fort Lighthouse\t', 'Dutch Reformed Church', 'Old Dutch Market\t', 'Dutch Hospital Shopping Precinct\t', 'Old Gate', 'Martin Wickramasinghe House & Folk Museum']
    df2 = pd.DataFrame(matrixHeritageAndHistoricalPlaces, index=rowsHeritagesHeritageAndHistoricalPlaces, columns=columnsHeritageHeritageAndHistoricalPlaces)
    
    matrixBeaches = np.zeros((1, 7))
    rowsBeaches = ['Avarage Distance']
    columnsBeaches = ['Jungle Beach', 'Unawatuna Beach', 'Hikkaduwa Beach', 'Dalawella Beach', 'Talpe Beach', 'Ahungalla Beach', 'Induruwa Beach']
    df3 = pd.DataFrame(matrixBeaches, index=rowsBeaches, columns=columnsBeaches)

    matrixParks = np.zeros((1, 4))
    rowsParks = ['Avarage Distance']
    columnsParks = ['Beach Park Galle Municipal Council', 'Mahamodara Beach Park Marine Walk', 'The Great wall of lovers galle', 'New Marine Walk Galle Sea sight']
    df4 = pd.DataFrame(matrixParks, index=rowsParks, columns=columnsParks)
    
    matrixArtGallary = np.zeros((1, 2))
    rowsArtGallaries = ['Avarage Distance']
    columnsArtGallaries = ['The Galle Fort Art Gallery', 'Pradeep Pencil Art Gallary']
    df5 = pd.DataFrame(matrixArtGallary, index=rowsArtGallaries, columns=columnsArtGallaries)
    # print("abc")
    data = pd.read_csv("/home/ubuntu/test/BACKEND/DataSet.csv") 
    
    # Temples = 3.0
    # Heritages = 4.0
    # Beaches = 6.0
    # StartLat = 6.0265776
    # StartLon = 80.21862858
    # EndLat = 5.9477618
    # EndLon = 80.4519634
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    start_positions = []
    final_start_positions = []
    time = 12
    start_positions.append(StartLat)
    start_positions.append(StartLon)

    while time > 0 and (Temples > 0 or Heritages > 0 or Beaches > 0 or Parks > 0 or Arts > 0):
        ProbArr = [Temples, Heritages, Beaches, Parks, Arts]

        if getMaxValue(ProbArr) == Temples:
            Temples *= 0.75

            if count1 == 0:
                findNeares(matrixTemple, StartLat, StartLon, EndLat, EndLon, df1)
                count1 +=1
                
            column_name_temple = df1.columns[find_min_value_position(matrixTemple)]
            
            galle_data_temple = data[data['Places'] == column_name_temple]
            latitude_col_temple = galle_data_temple['Latitude'].values[0]
            longitude_col_temple = galle_data_temple['Longitude'].values[0]
            start_positions.append(latitude_col_temple)
            start_positions.append(longitude_col_temple)
            # StartLat = latitude_col_temple
            # StartLon = longitude_col_temple
            
            time -= 1
        elif getMaxValue(ProbArr) == Heritages:
            Heritages *= 0.75
            
            if count2 == 0:
                findNeares(matrixHeritageAndHistoricalPlaces, StartLat, StartLon, EndLat, EndLon, df2)
                count2 += 1
            
            column_name_HeritageAndHistoricalPlaces = df2.columns[find_min_value_position(matrixHeritageAndHistoricalPlaces)]
            
            galle_data_column_name_HeritageAndHistoricalPlaces = data[data['Places'] == column_name_HeritageAndHistoricalPlaces]
            latitude_col_HeritageAndHistoricalPlaces = galle_data_column_name_HeritageAndHistoricalPlaces['Latitude'].values[0]
            longitude_col_HeritageAndHistoricalPlaces = galle_data_column_name_HeritageAndHistoricalPlaces['Longitude'].values[0]
            start_positions.append(latitude_col_HeritageAndHistoricalPlaces)
            start_positions.append(longitude_col_HeritageAndHistoricalPlaces)
            # StartLat = latitude_col_HeritageAndHistoricalPlaces
            # StartLon = longitude_col_HeritageAndHistoricalPlaces

            
            time -= 1
        elif getMaxValue(ProbArr) == Beaches:
            Beaches *= 0
            
            if count3 == 0:
                findNeares(matrixBeaches, StartLat, StartLon, EndLat, EndLon, df3)
                count3 += 1
            
            
            column_name_Beaches = df3.columns[find_min_value_position(matrixBeaches)]
            
            galle_data_column_name_Beaches = data[data['Places'] == column_name_Beaches]
            latitude_col_Beaches = galle_data_column_name_Beaches['Latitude'].values[0]
            longitude_col_Beaches = galle_data_column_name_Beaches['Longitude'].values[0]
            start_positions.append(latitude_col_Beaches)
            start_positions.append(longitude_col_Beaches)

            # StartLat = latitude_col_Beaches
            # StartLon = longitude_col_Beaches
            
            
            time -= 4
        elif getMaxValue(ProbArr) == Parks:
            Parks *= 0
            
            if count4 == 0:
                findNeares(matrixParks, StartLat, StartLon, EndLat, EndLon, df4)
                count4 += 1
            
            column_name_Parks = df4.columns[find_min_value_position(matrixParks)]
            
            galle_data_column_name_Parks = data[data['Places'] == column_name_Parks]
            latitude_col_Parks = galle_data_column_name_Parks['Latitude'].values[0]
            longitude_col_Parks = galle_data_column_name_Parks['Longitude'].values[0]
            start_positions.append(latitude_col_Parks)
            start_positions.append(longitude_col_Parks)
            
            time -= 2
        

        else:
            Arts *= 0.75
            
            if count5 == 0:
                findNeares(matrixArtGallary, StartLat, StartLon, EndLat, EndLon, df5)
                count5 += 1
            
            column_name_ArtGallary = df5.columns[find_min_value_position(matrixArtGallary)]
            
            galle_data_column_name_ArtGallary = data[data['Places'] == column_name_ArtGallary]
            latitude_col_ArtGallary = galle_data_column_name_ArtGallary['Latitude'].values[0]
            longitude_col_ArtGallary = galle_data_column_name_ArtGallary['Longitude'].values[0]
            start_positions.append(latitude_col_ArtGallary)
            start_positions.append(longitude_col_ArtGallary)
            
            time -= 2






    # start_positions.append(EndLat)
    # start_positions.append(EndLon)
    #.................................................................................

    list_size = len(start_positions)
    arr_size = list_size//2
    # print(arr_size)
    matrixNew = np.zeros((arr_size, arr_size))
    # print(matrixNew)
    

    # for i in range(len(start_positions)):
    #     print(start_positions[i], end=" ")

    newlen = len(start_positions) // 2

    arrz = [[0 for _ in range(newlen)] for _ in range(newlen)]
    for i in range(1):
        for j in range(1 + i, newlen):
            
            url3 = "http://router.project-osrm.org/route/v1/driving/" + str(start_positions[i + i + 1]) + "," + str(start_positions[i + i]) + ";" + str(start_positions[j + j + 1]) + "," + str(start_positions[j + j]) + "?overview=false"
            response3 = requests.get(url3).json()
            distance3 = response3["routes"][0]["distance"]
            
            arrz[i][j] = distance3
            
#             arrz[i][j] = start_positions[i + i] + start_positions[i + i + 1] + start_positions[j + j] + start_positions[j + j + 1]
            #arrz[j][i] = arrz[i][j]
#             print("The shortest road distance between", row_name, "and", column_name, "is", distance1, "meters.")


    minValue = 0
    # for row in arrz:
    #     for element in row:
    #         print(element, end=" ")
    #     print()  

    for j in range(newlen):
        minIndex = j
        for k in range(j + 1, newlen):
            if arrz[0][k] < arrz[0][minIndex]:
                minIndex = k
        # Swap elements in the sorted array
        arrz[0][j], arrz[0][minIndex] = arrz[0][minIndex], arrz[0][j]
        # Swap corresponding j values in the unsorted array
        start_positions[j + j], start_positions[minIndex + minIndex] = start_positions[minIndex + minIndex], start_positions[j + j]
        start_positions[j + j + 1], start_positions[minIndex + minIndex + 1] = start_positions[minIndex + minIndex + 1], start_positions[j + j + 1]

    # Print the sorted first row and corresponding j values from the unsorted array
    # print("Sorted first row:")
    for j in range(newlen):
        # print(arrz[0][j], "corresponding j value:", start_positions[j + j])
        # print(arrz[0][j], "corresponding j value:", start_positions[j + j + 1])
        final_start_positions.append(start_positions[j + j])
        final_start_positions.append(start_positions[j + j + 1])
    
    # print(final_start_positions)

    #.................................................................................
    final_start_positions.append(EndLat)
    final_start_positions.append(EndLon)
    print(EndLat)
    print(EndLon)
    return final_start_positions

def getMaxValue(ProbArr):
    max_value = ProbArr[0]
    for value in ProbArr:
        if value > max_value:
            max_value = value
    return max_value

def findNeares(disArr, StartLat, StartLon, EndLat, EndLon, df):
    data = pd.read_csv("/home/ubuntu/test/BACKEND/DataSet.csv") 
    for i in range(1):
        for j in range(len(disArr[0])):
            column_name = df.columns[j]
            galle_data_column = data[data['Places'] == column_name]
            latitude_col = galle_data_column['Latitude'].values[0]
            longitude_col = galle_data_column['Longitude'].values[0]
            
            row_name = df.index[i]
     
            import requests
            import json

            url1 = "http://router.project-osrm.org/route/v1/driving/" + str(longitude_col) + "," + str(latitude_col) + ";" + str(StartLon) + "," + str(StartLat) + "?overview=false"
            response1 = requests.get(url1).json()
            distance1 = response1["routes"][0]["distance"]
             
            
            url2 = "http://router.project-osrm.org/route/v1/driving/" + str(longitude_col) + "," + str(latitude_col) + ";" + str(EndLon) + "," + str(EndLat) + "?overview=false"
            response2 = requests.get(url2).json()
            distance2 = response2["routes"][0]["distance"]
            
            distence = distance1 + distance2 
            disArr[i][j] = distance1 + distance2 
            
def get_lowest_value(disArr):
    min_value = float('inf')  

    for row in disArr:
        for value in row:
            if value < min_value:
                min_value = value
                column_name = df1.columns[1]

    return min_value

def find_min_value_position(disArr):
    min_value = float('inf') 
    min_row = -1
    min_col = -1

    for row_idx, row in enumerate(disArr):
        for col_idx, value in enumerate(row):
            if value < min_value:
                min_value = value
                min_row = row_idx
                min_col = col_idx

    disArr[0][min_col] = 999999 
    return min_col

# Run the main function
# main()

@app.route('/users', methods=['GET','POST'])
def add_user():
    if request.method == 'GET':
        # Retrieve all users from the database
        users = db.users.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return jsonify({'users': user_list})

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        fristname = data.get('fristname')
        lastname = data.get('lastname')
        gender = data.get('gender')
        age = data.get('age')
        email = data.get('email')
        telephone = data.get('telephone')
        country = data.get('country')
        password = data.get('password')

        # Check if name and gender are provided
        if not username or not gender or not age or not email or not telephone or not country or not fristname or not lastname or not password:
            return jsonify({'message': 'All the data must be filled'}), 400
        
        existing_user = db.users.find_one({'username': username})
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        # Create a new user document
        user = {
            'username': username,
            'fristname' : fristname,
            'lastname' : lastname,
            'gender': gender,
            'age' : age,
            'email' : email,
            'telephone' : telephone,
            'country' : country,
            'password' : password
        }

        # Insert the user into the database
        result = db.users.insert_one(user)

        return jsonify({'message': 'User added successfully', 'user_id': str(result.inserted_id)})

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    # Retrieve the user from the database using the given username
    user = db.users.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Convert ObjectId to string for JSON serialization
    user['_id'] = str(user['_id'])

    return jsonify({'user': user})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Retrieve the user from the database based on the given username
    user = db.users.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the password provided matches the password in the database
    if user['password'] != password:
        return jsonify({'message': 'Invalid password'}), 401

    # If the username and password are correct, return a success message or any other data you want to provide to the user upon successful login
    return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])})


@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    # Check if the user with the given username exists in the database
    existing_user = db.users.find_one({'username': username})

    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    # Delete the user from the database
    db.users.delete_one({'username': username})

    return jsonify({'message': 'User deleted successfully'})

@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    # Retrieve the user from the database based on the given username
    existing_user = db.users.find_one({'username': username})

    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    # Get the updated user data from the request
    data = request.get_json()

    # Update the user's information
    existing_user['fristname'] = data.get('fristname', existing_user['fristname'])
    existing_user['lastname'] = data.get('lastname', existing_user['lastname'])
    existing_user['gender'] = data.get('gender', existing_user['gender'])
    existing_user['age'] = data.get('age', existing_user['age'])
    existing_user['email'] = data.get('email', existing_user['email'])
    existing_user['telephone'] = data.get('telephone', existing_user['telephone'])
    existing_user['country'] = data.get('country', existing_user['country'])
    existing_user['password'] = data.get('password', existing_user['password'])

    # Update the user in the database
    db.users.update_one({'username': username}, {'$set': existing_user})

    return jsonify({'message': 'User updated successfully'})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)