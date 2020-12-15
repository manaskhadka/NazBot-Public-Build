# this script parses through the urls given in the gacha library and prints them to the console
# debug tool
import json

image_list = []

with open('data/gacha.json') as file:
    gacha_dict = json.load(file)

gacha_dict_keys = gacha_dict.keys()

for key in gacha_dict_keys:
    image_list.append(gacha_dict[key][4])

for image in image_list:
    print(image)
