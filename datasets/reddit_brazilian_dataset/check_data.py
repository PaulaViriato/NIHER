import json
import os

def write_data (data):
    with open("complete_dataset.json", 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def open_file (name_file):
    data = {}
    with open(name_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

def open_files (data):
    data["statistics"]["num_subdirect"] = len(data["subdirectories"].keys())
    data["statistics"]["num_data"] = 0
    for key in data["subdirectories"].keys():
        data["statistics"][key] = {}
        data["statistics"][key]["num_files"] = len(data["subdirectories"][key]["files"])
        data["statistics"][key]["num_data"] = 0
        for file in data["subdirectories"][key]["files"]:
            jsondata = open_file(key+"/"+file)
            for j in jsondata["posts"]:
                data["subdirectories"][key]["data"].append(j)
                data["alldata"].append(j)
                data["statistics"][key]["num_data"] += 1
                data["statistics"]["num_data"] += 1
    return data

def all_subdirectories (path):
    walker = path
    if (len(walker) > 0):
        if (walker[-1] == '/'):
            walker = walker[:-1]
    data = {"statistics": {}, "alldata": [], "subdirectories": {}}

    for _, subdir, _ in os.walk(walker):
        for s in subdir:
            data["subdirectories"][walker+"/"+str(s)] = {}
            data["subdirectories"][walker+"/"+str(s)]["files"] = []
            data["subdirectories"][walker+"/"+str(s)]["data"] = []

    for key in data["subdirectories"].keys():
        for _, _, files in os.walk(key):
            for f in files:
                data["subdirectories"][key]["files"].append(f)
    return data

if __name__ == '__main__':
    data = all_subdirectories(str(input("Pasta: ")))
    data = open_files(data)
    write_data(data)