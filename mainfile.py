
import requests
import json
from urllib.request import urlopen
from flask import Flask,jsonify
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"






#api response
# @app.route("/get")
# def hello_world2():
#     return "<p>Hello222222, World!</p>"

@app.route("/get")
def get_info():
    with urlopen("https://ssd-api.jpl.nasa.gov/nhats.api") as response:
        print(1)
        source=response.read()
    data=json.loads(source)    
    dict_info=dict()
    count=0
    list_info=[]
    for item in data["data"]:
        dict_info=dict()
        if len(list_info)>49: break
        # count+=1
        # print(count)
        dict_info["type"]="Aestroid"
        dict_info["des"]=item["des"]
        dict_info["fullname"]=item["fullname"].strip()
        if not("2024" in  dict_info["fullname"]):
            continue
        dict_info["size"]=float(item["min_size"])+float(item["max_size"])/(2)
        # dict_info["max_size"]=
        dict_info["radius"]=dict_info["size"]/2
        dict_info["speed"]=float(item["min_dv"]["dv"])
        dict_info["timetaken"]=item["min_dv"]["dur"]
        a="%20".join(dict_info["des"].split())
        with urlopen(f"https://ssd-api.jpl.nasa.gov/nhats.api?des={a}") as data_aestroid:
            source_data=data_aestroid.read()
            data1=json.loads(source_data)
            dur_out=int(data1["min_dur_traj"]["dur_out"])*86400
            v_dep_earth=float(data1["min_dur_traj"]["v_dep_earth"])
            approx_distance_from_earth=(v_dep_earth*dur_out)
            # print(approx_distance_from_earth)
            dict_info["distance"]=approx_distance_from_earth
        list_info.append(dict_info)
        print(len(list_info))
    # for info in list_info:
    #     print(json.dumps(info,indent=3))
    print("done")
    result={"Asteroid_info":list_info}
    return jsonify(result)
# list_info=get_info(data)    
# with open("data.json","w") as f:
#     json.dump(list_info,f,indent=3)
if __name__=='__main__':
    app.run(debug=True)
