"""  
This script generates a text file with frame to frame location data, extracted from a GPS file 
  
Usage:
  add_gps_data.py <videosFolder> <idxFolder> <gpxFile> <outFolder> 
  add_gps_data.py -h | --help

Options:
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


# initial_loc: LatLon object
# ref_lst: list of [date, LatLon]
def get_location(date_, ref_ls):
    
    #print('date_', date_)
    #print('date_0', ref_lst[0][0])
    
    gps_tag = None    
    # Find the position of date_ between two elements of ref_lst (sorted list)
    count = 0
    while count < len(ref_lst) and date_ > ref_lst[count][0]:
        count = count + 1
    #print('date_count-1', ref_lst[count-1][0] )
    if count == 0 or count ==len(ref_lst):
        print('NONE')
        return None
    #print('COUNT value is', count)
    #print('1st assert: date_ >= date_0', date_ >= ref_lst[0][0])
    #print('2nd assert: date_ <= date_count-1 ', date_ <= ref_lst[count-1][0] )
    #print('List of dates all dates until count:')
    
    #for counter in range(count+1): 
        #print(ref_lst[counter][0])
    #print('end of for loop')
    assert date_ >= ref_lst[0][0] and date_ <= ref_lst[count][0]  
    date_ref_prev = ref_lst[count-1][0]
    gps_ref_prev  = ref_lst[count-1][1]
    gps_ref_next  = ref_lst[count][1]

    # Compute distance and heading using LatLon3 package
    dist = gps_ref_prev.distance(gps_ref_next, ellipse = 'sphere')
    initial_heading = gps_ref_prev.heading_initial(gps_ref_next, ellipse = 'sphere')

    # Compute temporal differences between current date and references
    td_prev  = date_ - date_ref_prev
    td_next  = ref_lst[count][0] - date_
    td_tot   = ref_lst[count][0] - date_ref_prev
    factor   = 1.0 if td_prev.total_seconds() == 0 else td_prev.total_seconds() / td_tot.total_seconds()  # Possible zero division error??
    
    td_threshold=20
    if td_prev.total_seconds() <= td_threshold and td_next.total_seconds() <= td_threshold: 
        # GPS coords
        gps_tag = gps_ref_prev.offset(initial_heading, dist * factor, ellipse = 'sphere')

    else:
        print ('No reference found')
        gps_tag = None

    return gps_tag

if __name__ == '__main__':
    # read arguments
    args = docopt(__doc__)
    
    videos_folder = args["<videosFolder>"]
    idx_folder    = args["<idxFolder>"]
    gpx_file      = args['<gpxFile>']
    out_folder    = args["<outFolder>"]

    utc = pytz.UTC
    
    ref_lst  = []    # List with gps info (time, position)
    #print (f'GPS file = {gpx_file}')

    gps_dict = Converter(input_file=gpx_file).gpx_to_dictionary(latitude_key='latitude', longitude_key='longitude')
    gps_time = gps_dict['time']
    gps_lati = gps_dict['latitude']
    gps_long = gps_dict['longitude']

    for tm, la, lo in zip(gps_time, gps_lati, gps_long):
        gps_loc  = latlon.LatLon(latlon.Latitude(la), latlon.Longitude(lo))
        ref_lst.append([tm, gps_loc])

    for file_ in os.listdir(videos_folder):
        if not file_.endswith(".mp4"):
            continue
        
        print (f'Converting {videos_folder}/{file_}')

        vid = ffmpeg.probe(f'{videos_folder}/{file_}')                       # Read metadata from video file
        #print("VID INFO:", vid)
        creation_time_str  = vid['format']['tags']['creation_time']          # Read creation_time metadata
        #print(creation_time_str)
        total_duration     = float(vid['format']['duration'])                # Read duration metadata
        location1          = vid['format']['tags']['location'] # Read GPS metadata. We assume it is in iso6709 string format: '+41.4068+002.1825/'
        #print('Location1:', location1)
        #print('Type location1:', type(location1))
        location = Location(location1)
        #print("")
        

        # Convert to datetime object
        creation_time = datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=utc)    # 2021-07-16T16:04:04.000000Z
        # Convert to LatLon3 object
        location      = latlon.LatLon(latlon.Latitude(location.lat.degrees),     latlon.Longitude(location.lng.degrees))

        # Read the associated idx file
        video_name, idx_ext = os.path.splitext(os.path.basename(file_))   
        idx_file_name = f'{idx_folder}/{video_name}.idx'

        out_idx = []
        data_ok = True
        
        for line in open(idx_file_name).read().splitlines():
            idx_line = line.split(' ')    # frame_number, frame_type, tmp, time_offset

            ts  = creation_time + timedelta(seconds=float(idx_line[3])) # Timestamp
            loc = get_location (ts, ref_lst)
            if not isinstance (loc, latlon.LatLon): # If no appropriate reference can be found, skip this video
                print (f'Warning!! Could not process video because of missing data for frame {idx_line[0]}')
                #data_ok = False
                #break
            else:
            #print (loc.lat, loc.lon)
            #print('tipo:', type(loc.lat))
                out_idx.append(' '.join(idx_line + [str(loc.lat), str(loc.lon)]))
            
        if data_ok:
            #add_gps_data.py <videosFolder> <idxFolder> <gpxFile> <outFolder> 
            #print("")
            #print("OUT_FOLDER:", out_folder)
            #print("IDX_FILE_NAME:", idx_file_name)
            # Save new idx file with location data
            
            out_idx_file_name = f'{out_folder}/{video_name}.idx'
            
            if out_idx:
                print("RUTA: ", out_idx_file_name )
                with open(out_idx_file_name, 'w') as fh:
                    for item in out_idx:
                        fh.write(f'{item}\n')

