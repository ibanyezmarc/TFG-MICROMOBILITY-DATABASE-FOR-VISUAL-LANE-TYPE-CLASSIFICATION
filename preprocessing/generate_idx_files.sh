#!/bin/bash


#
# Script to create .idx files, containing the relationship between timestamps and frame numbers
#
if [ $# -lt 2 ]; then
	echo "USAGE: generate_idx_files out_dir input_files 
    echo "       Example: $0 idx *.mp4
    exit
fi

OUT_DIR=$1
shift

for VIDEO_FILE in $@
	do
        BNAME=$(basename "$VIDEO_FILE" .mp4)
        OUTPUT_FILE=${OUT_DIR}/${BNAME}.idx
        
        echo "ffmpeg -i ${VIDEO_FILE} -filter:v \"showinfo\" -f null - 2>&1 | sed 's/\r/\n/' | grep pts_time | sed 's/:       /:/g' | sed 's/:      /:/g' | sed 's/:     /:/g' | sed 's/:    /:/g'  | sed 's/:   /:/g' | sed 's/:  /:/g' | sed 's/: /:/g' | awk '{print \$4 \" \" \$11 \" 0 \" \$6}' | sed 's/n://' | sed 's/pts_time://'  | sed 's/i://' > ${OUTPUT_FILE}"

        ffmpeg -i ${VIDEO_FILE} -filter:v "showinfo"    -f null - 2>&1 | sed 's/\r/\n/' | grep pts_time | sed 's/:       /:/g' | sed 's/:      /:/g' | sed 's/:     /:/g' | sed 's/:    /:/g'  | sed 's/:   /:/g' | sed 's/:  /:/g' | sed 's/: /:/g' | awk '{print $4 " " $11 " 0 " $6}' | sed 's/n://' | sed 's/pts_time://' | sed 's/i://' > "${OUTPUT_FILE}"
        
    done