import argparse
import datetime
import os

from pymediainfo import MediaInfo


def __parse_filename(utc_string, output_pattern, hour_offset):
    naive = datetime.datetime.strptime(utc_string, 'UTC %Y-%m-%d %H:%M:%S')
    naive += datetime.timedelta(hours=hour_offset)
    return naive.strftime(output_pattern)


def __rename(src, dst, retry=0):
    try:
        if retry == 0:
            os.rename(src, dst)
            print 'rename {} -> {}'.format(src, dst)
        else:
            dst_new = dst[:dst.rfind('.')] + '-{}'.format(retry) + dst[dst.rfind('.'):]
            os.rename(src, dst_new)
            print 'rename {} -> {}'.format(src, dst_new)
    except WindowsError:
        __rename(src, dst, retry + 1)


def main():
    parser = argparse.ArgumentParser(description='Rename all video files in a directory to their encoded dates.')
    parser.add_argument('-d', dest='directory', help='target directory', type=str, required=True)
    parser.add_argument('-p', dest='pattern', help='output pattern', type=str, required=True)
    parser.add_argument('-o', dest='offset', help='hours to shift', type=int, default=0)

    args = parser.parse_args()

    for f in os.listdir(args.directory):
        media_info = MediaInfo.parse(os.path.join(args.directory, f))
        for track in media_info.tracks:
            if track.track_type == 'Video':
                f_after = __parse_filename(track.encoded_date, args.pattern, args.offset) + f[f.rfind('.'):]
                __rename(os.path.join(args.directory, f), os.path.join(args.directory, f_after))


if __name__ == '__main__':
    main()
