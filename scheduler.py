import csv
import os
import subprocess
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Scheduler")
    parser.add_argument("--schedule", type=str,
                      help="schedule csv file")
    
    return parser.parse_args()

def check_parameter(args):
    if not os.path.isfile(args.schedule) or not (args.schedule).endswith('.csv'):
        raise AssertionError('Schedule file does not exist. We need a csv file')



if __name__ == '__main__':
    args = parser()
    check_parameter(args)

    print('-------RUN SCHEDULE FILE: {}'.format(os.path.abspath(args.schedule)))

    # Load csv file
    data_list = None
    with open(args.schedule, 'r',encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf)
        data_list = list(csvReader)
    
    # Create processes
    proc_list = list()
    for row in data_list:
        #print(row)
        command = "python collect_camera_frames.py --from_index {} --to_index {} --duration_per_cam {} --starting_hour {} --output_dir {} --cam_list {}" \
                    .format(row['from_index'], row['to_index'], row['duration_per_cam'], row['starting_hour'], row['output_dir'], row['cam_list'])
        print(command)
        p = subprocess.Popen(command.split(' '))
        proc_list.append(p)

    # Wait all of process finish
    for p in proc_list:
        p.wait()    

    print('-----------FINISH SCHEDULER-------------')