"""  
This script

Usage:
  modelsVideo.py [--modelType=<mt>]
  modelsVideo.py -h | --help
  
Options:
  --modelType=<mt>        Model used (3d or 2d) [default: 3d]
"""
from docopt import docopt
import pandas as pd

cont_shared_ok = 0
cont_crosswalk_ok = 0 
cont_bike_ok = 0
cont_sidewalk_ok = 0
cont_road_ok = 0
cont_shared = 0
cont_crosswalk = 0 
cont_bike = 0
cont_sidewalk = 0
cont_road = 0

def main():
    video_list2 = []
    cont = []
    first = True
    ok = True
    video_ok = 0
    num_videos = 0
    linia = 0
    if tipus_model == '2d':
        models = pd.read_csv("/home/usuaris/imatge/mireia.ambros/models_2d_T2F25_val_2021.csv")
    if tipus_model == '2d_2022':
        models = pd.read_csv("/home/usuaris/imatge/mireia.ambros/models_2d_T2F25_val_2022.csv")
    if tipus_model == '3d':
        models = pd.read_csv("/home/usuaris/imatge/mireia.ambros/models_3d_df.csv")
    if tipus_model == '3d_2022':
        models = pd.read_csv("models_3d_2022.csv")
    
    print(models.shape[0])

    for row in models.index:
        linia= linia+1
        print("linia",linia)
        print(models.loc[row, 'Filename'])
        if models.loc[row, 'Num of segment'] == 0 and first == True:
            if models.loc[row, 'Correct prediction segment'] == "No":
                ok = False
            cont.append(1)
            first = False
        
        elif models.loc[row, 'Num of segment'] != 0 and first == False:
            if models.loc[row, 'Correct prediction segment'] == "No":
                ok = False
            cont.append(1)
            if row == (models.index.size - 1):
                if ok == True:
                    for i in cont:
                        video_list2.append("Yes")
                        print(len(video_list2))
                    video_ok += 1
                    cont_class_ok(models.loc[row, 'Actual'])
                else:
                    for i in cont:
                        video_list2.append("No")
                        print(len(video_list2))
                num_videos += 1
                cont_class(models.loc[row, 'Actual'])

        elif models.loc[row, 'Num of segment'] == 0 and first == False:
            if ok == True:
                for i in cont:
                    video_list2.append("Yes")
                    print(len(video_list2))
                video_ok += 1
                cont_class_ok(models.loc[row, 'Actual'])
            else:
                for i in cont:
                    video_list2.append("No")
                    print(len(video_list2))
            num_videos += 1
            cont_class(models.loc[row, 'Actual'])
            cont.clear()
            ok = True
            if models.loc[row, 'Correct prediction segment'] == "No":
                ok = False
            cont.append(1)
            first=False
    print(models.index)    
    print("total ",len(video_list2))
    models['Correct prediction video'] = video_list2
    if tipus_model == '2d':
        models.to_csv('videos_2d_T2F25_val_2021.csv', index=None, columns=None)
        print("Num of correct videos: ", video_ok)
        print("Num of videos: ", num_videos)
        print("Accuracy (video evaluation): ", round((video_ok/num_videos)*100, 2), "%")
        print("Num of correct shared: ", cont_shared_ok)
        print("Num of shared: ", cont_shared)
        print("Accuracy (shared): ", round((cont_shared_ok/cont_shared)*100, 2), "%")
        print("Num of correct crosswalk: ", cont_crosswalk_ok)
        print("Num of crosswalk: ", cont_crosswalk)
        print("Accuracy (crosswalk): ", round((cont_crosswalk_ok/cont_crosswalk)*100, 2), "%")
        print("Num of correct bike: ", cont_bike_ok)
        print("Num of bike: ", cont_bike)
        print("Accuracy (bike): ", round((cont_bike_ok/cont_bike)*100, 2), "%")
        print("Num of correct sidewalk: ", cont_sidewalk_ok)
        print("Num of sidewalk: ", cont_sidewalk)
        print("Accuracy (sidewalk): ", round((cont_sidewalk_ok/cont_sidewalk)*100, 2), "%")
        print("Num of correct road: ", cont_road_ok)
        print("Num of road: ", cont_road)
        print("Accuracy (road): ", round((cont_road_ok/cont_road)*100, 2), "%")
    if tipus_model == '2d_2022':
        models.to_csv('videos_2d_T2F25_val_2022.csv', index=None, columns=None)
        print("Num of correct videos: ", video_ok)
        print("Num of videos: ", num_videos)
        print("Accuracy (video evaluation): ", round((video_ok/num_videos)*100, 2), "%")
        print("Num of correct shared: ", cont_shared_ok)
        print("Num of shared: ", cont_shared)
        print("Accuracy (shared): ", round((cont_shared_ok/cont_shared)*100, 2), "%")
        print("Num of correct bike: ", cont_bike_ok)
        print("Num of bike: ", cont_bike)
        print("Accuracy (bike): ", round((cont_bike_ok/cont_bike)*100, 2), "%")
        print("Num of correct sidewalk: ", cont_sidewalk_ok)
        print("Num of sidewalk: ", cont_sidewalk)
        print("Accuracy (sidewalk): ", round((cont_sidewalk_ok/cont_sidewalk)*100, 2), "%")
        print("Num of correct road: ", cont_road_ok)
        print("Num of road: ", cont_road)
        print("Accuracy (road): ", round((cont_road_ok/cont_road)*100, 2), "%")
    if tipus_model == '3d_2022':
        models.to_csv('videos_3d_2022.csv', index=None, columns=None)
        print("Num of correct videos: ", video_ok)
        print("Num of videos: ", num_videos)
        print("Accuracy (video evaluation): ", round((video_ok/num_videos)*100, 2), "%")
        print("Num of correct shared: ", cont_shared_ok)
        print("Num of shared: ", cont_shared)
        print("Accuracy (shared): ", round((cont_shared_ok/cont_shared)*100, 2), "%")
        print("Num of correct bike: ", cont_bike_ok)
        print("Num of bike: ", cont_bike)
        print("Accuracy (bike): ", round((cont_bike_ok/cont_bike)*100, 2), "%")
        print("Num of correct sidewalk: ", cont_sidewalk_ok)
        print("Num of sidewalk: ", cont_sidewalk)
        print("Accuracy (sidewalk): ", round((cont_sidewalk_ok/cont_sidewalk)*100, 2), "%")
        print("Num of correct road: ", cont_road_ok)
        print("Num of road: ", cont_road)
        print("Accuracy (road): ", round((cont_road_ok/cont_road)*100, 2), "%")
    if tipus_model == '3d':
        models.to_csv('models_videos_3d_df.csv', index=None, columns=None)
        print("Num of correct videos: ", video_ok)
        print("Num of videos: ", num_videos)
        print("Accuracy (video evaluation): ", round((video_ok/num_videos)*100, 2), "%")
        print("Num of correct shared: ", cont_shared_ok)
        print("Num of shared: ", cont_shared)
        print("Accuracy (shared): ", round((cont_shared_ok/cont_shared)*100, 2), "%")
        print("Num of correct crosswalk: ", cont_crosswalk_ok)
        print("Num of crosswalk: ", cont_crosswalk)
        print("Accuracy (crosswalk): ", round((cont_crosswalk_ok/cont_crosswalk)*100, 2), "%")
        print("Num of correct bike: ", cont_bike_ok)
        print("Num of bike: ", cont_bike)
        print("Accuracy (bike): ", round((cont_bike_ok/cont_bike)*100, 2), "%")
        print("Num of correct sidewalk: ", cont_sidewalk_ok)
        print("Num of sidewalk: ", cont_sidewalk)
        print("Accuracy (sidewalk): ", round((cont_sidewalk_ok/cont_sidewalk)*100, 2), "%")
        print("Num of correct road: ", cont_road_ok)
        print("Num of road: ", cont_road)
        print("Accuracy (road): ", round((cont_road_ok/cont_road)*100, 2), "%")
    

def cont_class_ok(value):
    if value == "shared":
        global cont_shared_ok
        cont_shared_ok += 1
    if value == "crosswalk":
        global cont_crosswalk_ok
        cont_crosswalk_ok += 1
    if value == "bike":
        global cont_bike_ok
        cont_bike_ok += 1
    if value == "sidewalk":
        global cont_sidewalk_ok
        cont_sidewalk_ok += 1
    if value == "road":
        global cont_road_ok
        cont_road_ok += 1

def cont_class(value):
    if value == "shared":
        global cont_shared
        cont_shared += 1
    if value == "crosswalk":
        global cont_crosswalk
        cont_crosswalk += 1
    if value == "bike":
        global cont_bike
        cont_bike += 1
    if value == "sidewalk":
        global cont_sidewalk
        cont_sidewalk += 1
    if value == "road":
        global cont_road
        cont_road += 1

if(__name__ == '__main__'):
     # read arguments
    args = docopt(__doc__)
    tipus_model  = args["--modelType"]
    main()