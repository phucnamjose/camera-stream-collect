import json
import csv
import os
import subprocess
import time
from datetime import datetime
import pytz
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Collect camera frames")
    parser.add_argument("--from_index", type=int,
                        help="from_index")
    parser.add_argument("--to_index", type=int,
                        help="to_index")
    parser.add_argument("--duration_per_cam", type=int,
                        help="duration_per_camera (second)")
    parser.add_argument("--starting_hour", type=int,
                        help="starting_hour (o\'clock)")
    parser.add_argument("--output_dir", type=str,
                      help="directory to save frames")
    parser.add_argument("--cam_list", type=str,
                      help="cameras json file")
    
    return parser.parse_args()

def check_parameter(args):
    assert args.duration_per_cam > 0 , f'Duration is a positive number, got: {args.duration_per_cam}'
    assert args.from_index > 0 , f'Index is a positive number, got: {args.from_index}'
    assert args.to_index > 0 , f'Index is a positive number, got: {args.to_index}'
    assert args.to_index > args.from_index, f'We run forward. not backward'
    if not os.path.isfile(args.cam_list) or not (args.cam_list).endswith('.json'):
        raise AssertionError('Camera list does not exist. We need a json file')

if __name__ == '__main__':
    args = parser()
    check_parameter(args)

    print('-------READ FROM INDEX: {} TO {}------'.format(args.from_index, args.to_index))
    print('-------START TIME: {} o\'clock in Maryland'.format(args.starting_hour))

    # Wait a time span
    while True:
        # Read the current data and time in Maryland
        datetime_in_Maryland = datetime.now(pytz.timezone('America/Virgin'))
        print('Now is: ', datetime_in_Maryland)
        print('Current hour: ', datetime_in_Maryland.hour)
        if datetime_in_Maryland.hour < args.starting_hour:
            print('Sleep 10 min then check time again')
            time.sleep(10*60)
            continue
        break

    print('-------START GETTING FRAME NOW------')

    # Create empty log file
    if not os.path.isdir(args.output_dir):
        # Create a new directory if it does not exist
        os.makedirs(args.output_dir)
    log_file = os.path.join(args.output_dir,'reading_log.csv')
    if not os.path.isfile(log_file):
        print('-----------CREATE NEW LOG FILE-------------')
        with open(log_file, 'a') as csv_file:
            data = {
                    "row_id": 'None',
                    "ID": 'None',
                    "fps": 'None',
                    "width": 'None',
                    "height": 'None',
                    "save_count": 'None',
                    "start_time": 'None',
                    "end_time": 'None'
                }
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data.keys())

    # Read camera metadata
    with open(args.cam_list) as json_file:
        data = json.load(json_file)
    cameras = data['features']

    # Operate
    camera_index = 0
    for camera in cameras:
        camera_index += 1
        # Skip don't-care camera
        if camera_index < args.from_index or camera_index > args.to_index:
            continue
        
        # Get ID and link
        properties = camera['properties']
        row_id = int(properties['rowid'])
        print('READ ROW ID {}'.format(row_id))
        camera_id = properties['ID']
        cameara_url = properties['url']
        command = "python stream2images.py --url {} --dont_show --camera_id {} --row_id {} --duration {} --output_dir {}" \
                .format(cameara_url, camera_id, row_id, args.duration_per_cam, args.output_dir)
        print(command)
        p = subprocess.run(command.split(' '))

    print('-----------FINISH COLLECTOR-------------')