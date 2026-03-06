from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random

from constants import *
import utils

app = FastAPI()

origins = ["*"]
socket_id  : int
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create usefull json files based on the data of the pictures
utils.group_json_by_levels()
utils.pictures_by_word()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/create_game")
def create_game(difficulty : int =1, n : int =3):
    """
    
    This GET endpoint returns n random words, with their
    respective n random images to find them
    and where are the objects in each image

    Arguments
    ----------
    difficulty : int 
        The level of difficulty of the vocabulary
        From 1 (easiest) to 4 (hardest)
    n : int
        The amount of questions


    """

    if (n<1):
        return
    if (n>MAX_QUESTIONS):
        n = MAX_QUESTIONS
    
    level = difficulty -1
    
    with open("ADE20K/levels_and_pics.json", "r") as j:
        levels_and_pics = json.load(j)

    if (n >= len(levels_and_pics[level])):
        n = len(levels_and_pics[level]) -1
    
    sample = random.sample(levels_and_pics[level], n)
    
    return_val = []

    for i in range(n):
        ann_path = random.sample(sample[i][1], 1)[0]
        vocab = sample[i][0]
        dict = {
            "vocab": vocab,
            "im_url": utils.ann_to_img_path(ann_path),
            "poligons": utils.find_poligons(vocab, ann_path)
        }
        return_val.append(dict)

    return { "game" : return_val,
            STATUS : SUCCESS }
