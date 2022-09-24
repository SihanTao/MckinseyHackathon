import pandas as pd
import json, requests, os
from tqdm import tqdm
from ImageSearch import Index,LoadData,SearchImage

def getPictureList(pictures: list, number=1):
    PREFIX = 'https://coimages.sciencemuseumgroup.org.uk/images/'
    res = []
    
    if number == 1:
        res.append(PREFIX + pictures[0]['processed']['large']['location'])
    else:
        for pic in pictures:
            res.append(PREFIX + pic['processed']['large']['location'])
    return res 

def getAllPictures(df, first=True):
    res = []
    n = len(df)
    for i in range(n):
        res += getPictureList(df.iloc[i]['attributes']['multimedia'], 1 if first else 0)
    return res 

def imageDownload(url_list):
    path = 'images/'
    os.makedirs(path, exist_ok=True)
    
    for i, image_url in tqdm(enumerate(url_list)):
        img_data = requests.get(image_url).content
        with open('images/' + str(i + 1) + '.jpg' , 'wb') as handler:
            handler.write(img_data)
            
            
with open('data.json') as json_data:
    data = json.load(json_data)

df = pd.DataFrame(data['data'])
imageDownload(getAllPictures(df))

input_image = 'sample_images/bicycle1.jpeg'
image_list = LoadData().from_folder(['images'])
# For Faster Serching we need to index Data first, After Indexing all the meta data stored on the local path
Index(image_list).Start()
# for searching you need to give the image path and the number of similar image you want
print(SearchImage().get_similar_images(image_path=input_image,number_of_images=5))
# If you want to plot similar images the you can use this method, It will plot 16 most similar images from the data index
# SearchImage().plot_similar_images(image_path = input_image)