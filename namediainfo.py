import datetime
import os
import sys

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
    target_dir = sys.argv[1]
    output_pattern = sys.argv[2]
    hour_offset = float(sys.argv[3])

    for f in os.listdir(target_dir):
        media_info = MediaInfo.parse(os.path.join(target_dir, f))
        for track in media_info.tracks:
            if track.track_type == 'Video':
                f_after = __parse_filename(track.encoded_date, output_pattern, hour_offset) + f[f.rfind('.'):]
                __rename(os.path.join(target_dir, f), os.path.join(target_dir, f_after))


if __name__ == '__main__':
    main()
