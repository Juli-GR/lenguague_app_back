import json
from pathlib import Path

from constants import *


"""
creates level.json:
groups the object classes in meta.json by difficulty
for example, with two levels of difficulty:
levels = [
    ["door", "table"],      <-- level 0
    ["rug", "sculpture"]    <-- level 1
]
"""
def group_json_by_levels():

    levels = [[] for _ in range(LEVELS)]

    with open("ADE20K/meta.json", "r") as j:
        j_ojects = json.load(j)
    
    for obj in j_ojects["classes"]:
        if obj["difficulty"]!=-1:
            level = obj["difficulty"] -1
            levels[level].append(obj["title"])
    
    with open('ADE20K/levels.json', 'w', encoding='utf-8') as f:
        json.dump(levels, f, indent=4, ensure_ascii=False)


"""
creates levels_and_pics.json:
for each vocab in levels.json
finds the images that have the object
and saves it in a similar file as levels.json
but instead of words has pairs (word, [pics])

this is highly inefficient if used with lots of images
improve if necessary
"""
def pictures_by_word():

    # Create a list of tuples (vocab, [pics]), by level
    levels_and_pics = [[] for _ in range(LEVELS)]
    with open("ADE20K/levels.json", "r") as j:
        j_levels = json.load(j)
        for i, level in enumerate(j_levels):
            for vocab in level:
                levels_and_pics[i].append((vocab, []))
    
    # Find the images for each object
    annotations = Path("ADE20K/ann")
    for ann_path in annotations.iterdir():
        if ann_path.is_file():
            with open(ann_path, "r") as ann:
                j_ann = json.load(ann)
                for obj in j_ann["objects"]:
                    for level in levels_and_pics:
                        for (vocab, pics) in level:
                            if vocab == obj["classTitle"] and (len(pics)==0 or pics[-1] != str(ann_path)):
                                pics.append(str(ann_path))
    
    # Remove duplicates
    final_levels_and_pics = [[] for _ in range(LEVELS)]
    for i, level in enumerate(levels_and_pics):
        for t in level:
            if t[1] != []:
                final_levels_and_pics[i].append(t)
                
    # Dump in json file
    with open('ADE20K/levels_and_pics.json', 'w', encoding='utf-8') as f:
        json.dump(final_levels_and_pics, f, indent=4, ensure_ascii=False)


"""
transform ann_path to img_path
example:
ADE20K\\ann\\ADE_train_00000126.json  ->  ADE20K\\img\\ADE_train_00000126.jpg
"""
def ann_to_img_path(ann_path):
    ann_path = ann_path.replace("json", "jpg")
    ann_path = ann_path.replace("ann", "img")
    return ann_path

"""
find every poligon in the json file of the ann_path
where <vocab> appears
a poligon has an external side and an interal side
"""
def find_poligons(vocab, ann_path):

    poligons = []

    with open(ann_path, "r") as j:
        ann = json.load(j)
    
    for obj in ann["objects"]:

        # Check if it is polygon, (what other options are there tho??)
        if (obj["geometryType"] != "polygon"):
            raise ValueError(f"geometryType is {obj["geometryType"]}, not polygon")
        
        # if it is the same type, add it to the list
        if (obj["classTitle"] == vocab):
            poligons.append(obj["points"])

    return poligons
