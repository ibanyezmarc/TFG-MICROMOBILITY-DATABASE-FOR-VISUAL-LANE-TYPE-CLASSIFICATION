#!/bin/bash


# Script de prueba


echo "split videos de input/sidewalk a output_split y output_split_no_idx, con carpeta location"
FOLDER=location/*.gpx

for FILE_1 in $FOLDER
do 
	python split_videos_2.py /mnt/gpid08/datasets/micromobility/lane_classification/ridesafe/barcelona/videos/sidewalk ./output_split ./output_split_no_idx  --splitSeconds=14 --gpxFile="$FILE_1"
done


echo "iterar todos los ficheros de output_split y sacar idx sin coordeanadas en output_idx:"
FOLDER_2=output_split/*.mp4

for FILE_2 in $FOLDER_2
do 
	echo "generating idx of $FILE_2"
	bash generate_idx_files.sh output_idx $FILE_2
done


echo "iterar todos los ficheros de output_idx y sacar idx con coordenadas añadidas, con carpeta location"
FOLDER_3=location/*.gpx

for FILE_3 in $FOLDER_3
do 
	python add_gps_data_2.py ./output_split ./output_idx "$FILE_3" ./output_gps
done


echo "quitar de output_split_no_idx los ficheros duplicados de output_split"
FOLDER_4=output_split/*.mp4

for FILE_4 in $FOLDER_4
do
	base_name=$(basename ${FILE_4})
	rm ./output_split_no_idx/"$base_name"
done