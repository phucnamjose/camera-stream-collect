import os
import cv2
from datetime import datetime
import pytz
import time
import argparse
import csv

def parser():
    parser = argparse.ArgumentParser(description="Reading stream video")
    parser.add_argument("--url", type=str, default=0,
                        help="video source link")
    parser.add_argument("--camera_id", type=str, default="",
                        help="camera id")
    parser.add_argument("--row_id", type=str, default="",
                        help="row id")
    parser.add_argument("--duration", type=int, default="",
                        help="time for getting frame (second)")
    parser.add_argument("--output_dir", type=str, default="",
                      help="directory to save frames")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown display. For headless systems")
    
    return parser.parse_args()

out_subdir = ''
def check_parameter(args):
    assert args.duration > 0 , f'Duration is a positive number, got: {args.duration}'
    sub_dir = '{}_{}'.format(args.row_id, args.camera_id)
    global out_subdir
    out_subdir = os.path.join(args.output_dir, sub_dir)
    if not os.path.isdir(out_subdir):
        # Create a new directory if it does not exist
        os.makedirs(out_subdir)
    

def video_capture():
    fps = 10
    if video_fps > 15:
        fps = 20
    #fps = 1
    save_count = 0
    frame_count = 0
    start_time = datetime.now(pytz.timezone('America/Virgin')).timestamp()
    file_prefix = '{}_{}_{}_'.format(args.row_id, args.camera_id, int(start_time))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break 
        frame_count = frame_count + 1
        if (frame_count % fps == 0):
            filename = file_prefix + str(save_count) + '.jpg'
            global out_subdir
            cv2.imwrite(os.path.join(out_subdir, filename), frame)
            save_count = save_count + 1
            if not args.dont_show:
                cv2.imshow('Stream', frame)
            #print('FRAME {}'.format(save_count))
        current_time = datetime.now(pytz.timezone('America/Virgin')).timestamp()
        #print(current_time)
        # Stop condition
        if (current_time - start_time) > args.duration:
            break
    print('GOT-: {} FRAME'.format(save_count))
    return save_count
      
if __name__ == '__main__':
    args = parser()
    check_parameter(args)
    input_path = args.url
    cap = cv2.VideoCapture(input_path)
    # Get information of Video
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print('Video FPS : {}, Size: {} x {}'.format(video_fps, width, height))
    print('-----------READING DURATION-: {} s'.format(args.duration))
    start_time = datetime.now(pytz.timezone('America/Virgin')).strftime("%Y-%m-%d %H:%M:%S")
    save_count = video_capture()
    end_time = datetime.now(pytz.timezone('America/Virgin')).strftime("%Y-%m-%d %H:%M:%S")
    # Save fps
    with open(os.path.join(args.output_dir,'reading_log.csv'), 'a') as csv_file: 
        csv_writer = csv.writer(csv_file)
        data = {
                "row_id": args.row_id,
                "ID": args.camera_id,
                "fps": video_fps,
                "width": width,
                "height": height,
                "save_count": save_count,
                "start_time": start_time,
                "end_time": end_time
            }
        csv_writer.writerow(data.values())
    
    cap.release()
    cv2.destroyAllWindows()  
    print('-----------END CAPTURING-------------')