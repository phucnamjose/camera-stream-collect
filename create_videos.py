import csv
import os
import subprocess
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Scheduler")
    parser.add_argument("--target_dir", type=str,
                      help="target dir consist multiple image subdir and a csv reading_log file")
    
    return parser.parse_args()

def check_parameter(args):
    if not os.path.isdir(args.target_dir): 
        raise AssertionError('Schedule file does not exist. We need a csv file')
    if not os.path.isfile(os.path.join(args.target_dir, 'reading_log.csv')):
        raise AssertionError('CSV reading_log file is not found')

if __name__ == '__main__':
    args = parser()
    check_parameter(args)

    print('-------TARGET DIR: {}'.format(os.path.abspath(args.target_dir)))

    # Load csv file
    data_list = None
    with open(os.path.join(args.target_dir, 'reading_log.csv'), 'r',encoding='utf-8-sig') as csvf: 
        csvReader = csv.DictReader(csvf)
        data_list = list(csvReader)
    
    # Call ffmpeg
    for row in data_list:
        # Check if subdir exists
        subdir_name = '{}_{}'.format(row['row_id'], row['ID'])
        subdir = os.path.join(args.target_dir, subdir_name)
        if not os.path.isdir(subdir):
            continue

        # Find image prefix of an image
        image_prefix = ''
        for image in os.listdir(subdir):
            if image.endswith('.jpg'):
                name_parts = image.split('_')
                order_part = name_parts[-1]
                image_prefix = image[:(len(image) - len(order_part) - 1)]
                print(image_prefix)
                break

        # Create video       
        image_pattern = '{}_%d.jpg'.format(image_prefix)
        images_name = os.path.join(subdir, image_pattern)
        video_name = '{}.mp4'.format(os.path.join(args.target_dir, image_prefix))
        command = "ffmpeg -framerate {} -i {} -c:v libx264 -r {} -pix_fmt yuv420p {}" \
                    .format(row['fps'], images_name, row['fps'], video_name)
        print(command)
        p = subprocess.run(command.split(' '))

    print('-----------FINISH CREATING VIDEOS-------------')