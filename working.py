import requests
import json
from urllib.request import urlopen
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getdata/")
def get_info():
    # Fetching the data from NASA NHATS API
    with urlopen("https://ssd-api.jpl.nasa.gov/nhats.api") as response:
        source = response.read()
    data = json.loads(source)

    list_info = []
    
    for item in data["data"]:
        dict_info = {}
        
        # Only include 50 asteroids
        if len(list_info) > 49:
            break
        
        dict_info["type"] = "Asteroid"
        dict_info["des"] = item["des"]
        dict_info["fullname"] = item["fullname"].strip()
        
        # Only process asteroids containing "2024" in their fullname
        if "2024" not in dict_info["fullname"]:
            continue
        
        # Calculate size and radius
        dict_info["size"] = (float(item["min_size"]) + float(item["max_size"])) / 2
        dict_info["radius"] = (float(item["min_size"]) + float(item["max_size"])) / 4
        
        # Extracting speed and time taken
        dict_info["speed"] = float(item["min_dv"]["dv"])
        dict_info["timetaken"] = item["min_dv"]["dur"]
        
        # Additional API call to fetch more information
        a = "%20".join(dict_info["des"].split())
        try:
            with urlopen(f"https://ssd-api.jpl.nasa.gov/nhats.api?des={a}") as data_asteroid:
                source_data = data_asteroid.read()
                data1 = json.loads(source_data)
                
                # Calculate approximate distance from Earth
                dur_out = int(data1["min_dur_traj"]["dur_out"]) * 86400  # convert days to seconds
                v_dep_earth = float(data1["min_dur_traj"]["v_dep_earth"])
                approx_distance_from_earth = v_dep_earth * dur_out
                dict_info["distance"] = approx_distance_from_earth
                
        except Exception as e:
            dict_info["distance"] = "Data not available"
        
        # Add asteroid data to the list
        list_info.append(dict_info)
    print("done")
    # Return the list of asteroids as a JSON response
    result = {"data": list_info}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
