READ ME to split videos and create idx files:


Command:
	bash automatic_for.sh


Scripts needed:
	add_gps_data_2.py
	automatic_for.sh
	generate_idx_files.sh
	split_videos_2.py
	

Folders needed in current directory:
	output_gps (empty)
	output_idx (empty)
	output_split (empty)
	output_split_no_idx (empty)
	input (or external source with videos that we can change in automatic_for.sh)
	location (with al gpx files or external source that we can change in automatic_for.sh)



Extra info:
	.idx final results in /output_gps
	split videos results in /output_split and /output_split_no_idx
	we can change different parameters in the automatic_for.sh:
		- input of the videos folder in the first "for"
		- seconds to split in the first "for"
		- location folder directory before first and third "for"
	venv: /home/usuaris/imatge/marc.ibanyez/venv/myenv/bin/activate
