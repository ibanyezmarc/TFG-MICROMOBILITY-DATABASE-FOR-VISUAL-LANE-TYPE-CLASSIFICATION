
"""  
This script splits a video in subclips
  
Usage:
  split_video.py <videosFolder> <outFolder> <outFolder_no_idx> [--videosExt=<ve>] [--splitSeconds=<ss>] [--deadTime=<dt>] [--gpxFile=<gp>]
  split_video.py -h | --help

Options:
  --videosExt=<ve>           Extension of the video files [default: .mp4]
  --splitSeconds=<ve>        Maximum number of seconds of the resulting subclips [default: 15]
  --deadTime=<dt>            Minimum number of seconds separating subclips [default: 3]
  --gpxFile=<gp>             Name of the GPS track file in GPX format [default: None]
"""

from docopt import docopt
import os
import subprocess
import ffmpeg
import datetime
from gpx_converter import Converter
import latlon
from datetime import timedelta
from datetime import datetime
from iso6709 import Location

import pytz                        # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
                                   # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
import sys



def sign_str(x):
    return '+' if x>=0 else '-'


def read_gpx_file (gpx_file):
    ref_lst  = []    # List with gps info (time, position)

    gps_dict = Converter(input_file=gpx_file).gpx_to_dictionary(latitude_key='latitude', longitude_key='longitude')
    gps_time = gps_dict['time']
    gps_lati = gps_dict['latitude']
    gps_long = gps_dict['longitude']

    for tm, la, lo in zip(gps_time, gps_lati, gps_long):
        gps_loc  = latlon.LatLon(latlon.Latitude(la), latlon.Longitude(lo))
        ref_lst.append([tm, gps_loc])

    return ref_lst


# initial_loc: LatLon object
# ref_lst: list of [date, LatLon]
def get_location_from_time(date_, initial_date, initial_loc, ref_lst, dist_threshold = 100, td_threshold=20):
    
    assert date_ >= initial_date

    gps_tag = None    
    # Find the position of date_ between two elements of ref_lst (sorted list)
    count = 0
    while count < len(ref_lst) and date_ > ref_lst[count][0]:
        count = count + 1

    if count > 0 and count < len(ref_lst):
        date_ref_prev = ref_lst[count-1][0] if ref_lst[count-1][0] > initial_date else initial_date
        gps_ref_prev  = ref_lst[count-1][1] if ref_lst[count-1][0] > initial_date else initial_loc        
        gps_ref_next  = ref_lst[count][1]

        # Compute distance and heading using LatLon3 package
        dist = gps_ref_prev.distance(gps_ref_next, ellipse = 'sphere')
        initial_heading = gps_ref_prev.heading_initial(gps_ref_next, ellipse = 'sphere')

        # Compute temporal differences between current date and references
        td_prev  = date_ - date_ref_prev
        td_next  = ref_lst[count][0] - date_
        td_tot   = ref_lst[count][0] - date_ref_prev
        factor   = 1.0 if td_prev.total_seconds() == 0 else td_prev.total_seconds() / td_tot.total_seconds()  # Possible zero division error??
        
        if dist < dist_threshold:
            # GPS coords
            gps_tag = gps_ref_prev.offset(initial_heading, dist * factor, ellipse = 'sphere')
            print ('using gps_ref_prev and gps_ref_next points: {} && {}'.format(ref_lst[count-1][1].to_string(), ref_lst[count][1].to_string()))

        elif td_prev.total_seconds() < td_threshold:
            # GPS coords
            gps_tag = gps_ref_prev
            print ('using gps_ref_prev point: {}'.format(ref_lst[count-1][1].to_string()))
        elif td_next.totsl_seconds() < td_threshold:
            # GPS coords
            gps_tag = gps_ref_next
            print ('using next point: {}'.format(ref_lst[count][1].to_string()))
        else:
            print ('No reference found')
            gps_tag = None

    elif count == 0:   # Start date is BEFORE any date in ref_lst
        td_next      = ref_lst[0][0] - date_
        gps_ref_next = ref_lst[0][1]
        if td_next.total_seconds() < td_threshold:
            # GPS coords
            gps_tag     = gps_ref_next
            print ('using gps_ref_next point'.format(ref_lst[count][1].to_string()))
        else:
            print ('No reference found')
            gps_tag = None
    else:               # Start date if AFTER all data in ref_lst
        td_prev      = date_ - ref_lst[count-1][0]
        gps_ref_prev = ref_lst[count-1][1]
        if td_prev.total_seconds() < td_threshold:
            # GPS coords
            gps_tag  = gps_ref_prev

            print ('using gps_ref_prev point'.format(ref_lst[count-1][1].to_string()))
        else:
            print ('No reference found')
            gps_tag = None
        
    return gps_tag

if __name__ == '__main__':
    # read arguments
    args = docopt(__doc__)
    
    videos_folder        = args["<videosFolder>"]
    out_folder           = args["<outFolder>"]
    out_folder_no_idx    = args["<outFolder_no_idx>"]
    videos_ext           = args['--videosExt']
    max_sec              = int(args['--splitSeconds'])
    dead_time            = int(args['--deadTime'])
    gpx_file             = args['--gpxFile']
    dead_time_orig       = dead_time
    
    print(' ')
    print(' ')
    print('START DOCOPT')
    print(' ')
    print(' ')
    print(' Dead time: ', dead_time)

    utc = pytz.UTC

    
    ref_lst  = []    # List with gps info (time, position)
    if gpx_file != 'None':
        print (f'Reading location data from {gpx_file}')
        ref_lst = read_gpx_file(gpx_file)
    
    for file_ in os.listdir(videos_folder):
        if file_.endswith(videos_ext):
            try:
                dead_time = dead_time_orig
                print(' ')
                print(' ')
                print('2nd START: file is ', file_)
                print(' Dead time: ', dead_time)
                print(' ')
                print(' ')
                print (f'Converting {videos_folder}/{file_}')

                vid = ffmpeg.probe(f'{videos_folder}/{file_}')                       # Read metadata from video file
                creation_time_str  = vid['format']['tags']['creation_time']          # Read creation_time metadata
                print("CREATION TIME IS:", creation_time_str)
                total_duration     = float(vid['format']['duration'])                # Read duration metadata
                location           = Location(vid['format']['tags']['location'])     # Read GPS metadata. We assume it is in iso6709 string format: '+41.4068+002.1825/'
                location_eng       = Location(vid['format']['tags']['location-eng']) # Read GPS metadata
                print("TIPO DE DATO:", type(vid['format']['tags']['location']))
                print("FIRST LOCATION IS:", vid['format']['tags']['location'])
                print("SECOND LOCATION IS:", location)
                #Convert to latlon3 format
                location     = latlon.LatLon(latlon.Latitude(location.lat.degrees),     latlon.Longitude(location.lng.degrees))
                location_eng = latlon.LatLon(latlon.Latitude(location_eng.lat.degrees), latlon.Longitude(location_eng.lng.degrees))
                print("CONVERTED LOCATION IS:", location)
                print("LOCATION_ENG IS:", location_eng)
            
                max_clips = int(total_duration // max_sec)                           # Maximum number of subclips
                rem       = total_duration % max_sec                                 # Remaining time
            
                print (f'Duration: {total_duration}, Max clips: {max_clips}')
                print('tipo de max_clips: ', type(max_clips))
                print('rem: ', rem)
                print('dead time: ', dead_time)
                if max_clips > 1:
                    print('primer if max_clips>1')
                    if rem / (max_clips-1) < dead_time:                              # We want to leave some time between subclips
                        print('primer if max_clips>1, segundo if')
                        max_clips = max_clips-1
                        rem = total_duration - max_clips * max_sec
                        print('max_clips 2: ', max_clips)
                        print('rem 2: ', rem)

                if max_clips >= 1: # If only one subclip is possible, leave the full length
                    print('segundo if max_clips>1')
                #[dt,ts] = creation_time.split('T') # The format of creation_time is '2021-07-15T16:27:09.000000Z'
                #ts      = ts[0:-1]                 # Remove last 'Z' character
                # Convert creation_time ts to seconds
                #ct_secs = sum(int(float(x)) * 60 ** i for i, x in enumerate(reversed(ts.split(':'))))

                    creation_time = datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=utc)    # 2021-07-16T16:04:04.000000Z
                
                    if max_clips >1:
                    # Actual time between subclips
                        dead_time = rem / (max_clips-1) 

                    start = 0
                    end   = max_sec
                    for ii in range (max_clips):
                        # New metadata to insert in the subclip
                        print('empieza for para cada subclip')
                        new_creation_time = creation_time + timedelta(seconds=start)
                        print("")
                        print('NEW_CREATION_TIME IS', new_creation_time)
                        print('NEW_CREATION_TIME datetime IS', new_creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
                        print("")
                        # Get the coordinates of the initial frame of the subclip
                        if len(ref_lst) != 0:   # If GPS data is available
                            print("HAY REF_list")
                            new_location     = get_location_from_time(new_creation_time, creation_time, location, ref_lst)
                            print(' ')
                            print(' ')
                            print('GPS_TAG is ', new_location)
                            print(' ')
                            print(' ')
                        
                            new_location_eng = new_location
                    
                        str_start_sc = str(timedelta(seconds=start))  # Timestamp of the subclip start
                        str_dur_sc   = str(timedelta(seconds=end))    # Duration (in seconds) of the subclip

                        # Update for next subclip
                        start     = start + max_sec + dead_time
                        end       = max_sec

                        print (f'Subclip {ii}: creation_time: {new_creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}, start: {str_start_sc}, dur: {str_dur_sc}')
                        new_creation_time_format = new_creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                        if new_location is not None:
                            str_new_location = f'{sign_str(float(new_location.lat))}{float(new_location.lat)}{sign_str(float(new_location.lon))}{float(new_location.lon)}/'
                            print('GPS_TAG new is ', str_new_location)
                        
                        bname,ext = os.path.splitext(os.path.basename(file_))
                        
                        
                        opti  = ['ffmpeg', '-y' , '-i', f'{videos_folder}/{file_}']
                        opti += ['-ss',  f'{str_start_sc}', '-t', f'{str_dur_sc}']                                     # Info to cut the subclip
                        opti += ['-c', 'copy', '-an']                                                                  # Copy (do not transcode) video stream
                        opti += ['-map_metadata', '0']                                                                 # Copy all the metadata
                        opti += ['-metadata', f'creation_time={new_creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}'] # Update creation time. Format is 2021-07-16T16:04:04.000000Z
                        opti += ['-movflags', 'use_metadata_tags'] 
                    
                        path_1 = [f'{out_folder}/{bname}_{ii}{ext}']    #store path i 
                        if len(ref_lst) != 0:   # If GPS data is available
                            if new_location is not None:
                                print("adding location")
                                opti += ['-metadata', f'location={str_new_location}']                                  # Update location
                                opti += ['-metadata', f'location-eng={str_new_location}']                              # Update location
                                opti += [f'{out_folder}/{bname}_{ii}{ext}']                                                              # Output file
                                print(' '.join(opti))
                                print('DONE:')
                                subprocess.run(opti)
                            else:       #if gps is None, there is no possibility to add gps data in the idx file in the future. We add them to another folder
                                print("no location added")
                                opti += [f'{out_folder_no_idx}/{bname}_{ii}{ext}']
                        else:           #if gps data is not available, there is no possibility to add gps data in the idx file in the future. We add them to another folder
                            print("no gps data available")
                            opti += [f'{out_folder_no_idx}/{bname}_{ii}{ext}']
                            
                        print(' '.join(opti))
                        print('DONE:')
                        subprocess.run(opti)   
            except:
                print("ERROR!")
                            