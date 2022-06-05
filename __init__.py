from flask import Flask, request, render_template
from datetime import datetime
import numpy as np

hourly_sounds = {}
hourly_lights = {}

def getData(path):
    path_to_file = path
    data = np.genfromtxt(path_to_file, delimiter='\n',dtype=None,encoding = None)
    lights = {}
    sounds = {}
    for i in data:
        line = i[2:len(i)-2].split(',')
        key = line[0][11:len(line[0])-7]
        light = int(line[1][2:len(line[1])-1])
        sound = int(line[2][2:len(line[2])])

        if(key in lights):
            lights[key][0] += light
            lights[key][1] += 1
        else:
            lights[key] = [light,1]

        if key in sounds:
            sounds[key][0] += sound
            sounds[key][1] += 1
        else:
            sounds[key] = [sound,1]

    for i, j in sounds.items():
        sounds[i] = j[0]/j[1]

    for i, j in lights.items():
        lights[i] = j[0]/j[1]

    labels = sounds.keys()
    valuesA = sounds.values()
    valuesB = lights.values()

    return (labels,valuesA,valuesB)
  
  
def fillDict(a):
    global hourly_sounds
    global hourly_lights
    date = a[0]
    light = a[1]
    sound = a[2]
    key = date[14:len(date)-3]

    hourly_sounds[key] = sound
    hourly_lights[key] = light


app = Flask(__name__)

vals = [("N/A","N/A","N/A")]

@app.route("/data", methods = ["POST", "GET"])
def data():
    global vals
    if request.method == "POST":
        value = request.form.get('Save Data')
        if(value=="SAVE DATA" or len(vals)>=500):
            f = open("data_friday.txt", "a")
            for i in vals:
                f.write(str(i)+"\n")
            f.close()
            vals = [("N/A","N/A","N/A")]
            return render_template('data.html', d = vals)
        else:
            if vals==[("N/A","N/A","N/A")]:
                vals = []
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            a = [dt_string]
            for i,j in request.args.items():
                a.append(str(j))

            fillDict(a)
            vals.append((a[0],a[1],a[2]))
            return render_template('data.html', d = vals)
    else:
        return render_template('data.html', d = vals)
      
@app.route("/home", methods = ["GET"])
def home():
    global hourly_lights
    global hourly_sounds
    focus = vals[len(vals)-1]
    if focus == ("N/A","N/A","N/A"):
        focus = (0,0,0)
    focal = []
    if int(focus[2]) <=500:
        focal.append("quiet")
    elif int(focus[2]) <= 900:
        focal.append("Moderate")
    else:
        focal.append("LOUD!!!!")

    if(int(focus[1]) <=300):
        focal.append("Dark")
    elif(int(focus[1]) <= 800):
        focal.append("Well Lit")
    else:
        focal.append("BRIGHT!!")
    """
    keys = hourly_lights.keys()
    valuesA = hourly_sounds.values()
    valuesB = hourly_lights.values()
    m = 0
    if(hourly_lights):
       m = max([max(hourly_sounds.values()),max(hourly_lights.values())])
    """

    return render_template('home.html', current = focal, title = "Past Hour Activity", max = 3000, labels = hourly_lights.keys(), valuesA = hourly_sounds.values(), valuesB = hourly_lights.values())


@app.route("/past/monday", methods = ["GET"])
def pastA():

    path_to_file = 'data_monday.txt'
    data = getData(path_to_file)
    m = max([max(data[1]),max(data[2])])
    return render_template('past.html', title='Monday Analysis', max=m, labels=data[0], valuesA=data[1], valuesB = data[2])


@app.route("/past/sunday", methods = ["GET"])
def pastB():
    path_to_file = 'data.txt'
    data = getData(path_to_file)
    m = max([max(data[1]),max(data[2])])
    return render_template('past.html', title='Sunday Analysis', max=m, labels=data[0], valuesA=data[1], valuesB = data[2])

