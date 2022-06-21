This is the code used to test the different models.

GENERAL DESCRIPTION:
	- models.py: will create a csv with the results of segment evaluation and plot a confusion matrix
	- modelsvideo.py: will write in the terminal the results of video evaluation


EXECUTION COMMAND EXAMPLE:
	- models.py: srun --time=10:00:00 -c 6 --mem 10 python models.py --modelType='3d_2022' --segmentDuration=1
	- modelsvideo.py: python modelsVideo.py --modelType='3d_2022'
