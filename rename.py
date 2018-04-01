import datetime
import os

from pymediainfo import MediaInfo

videos_dir = './videos/'
hours_delta = -7


def __parse_filename(utc_string):
    naive = datetime.datetime.strptime(utc_string, "UTC %Y-%m-%d %H:%M:%S")
    naive += datetime.timedelta(hours=hours_delta)
    return naive.strftime("%Y%m%d_%H%M%S")


def __rename(src, dst, retry=0):
    try:
        if retry > 0:
            dst = dst[:dst.rfind('.')] + '-{}'.format(retry) + dst[dst.rfind('.'):]
        os.rename(src, dst)
        print 'rename {} -> {}'.format(src, dst)
    except WindowsError:
        __rename(src, dst, retry + 1)


def main():
    for f in os.listdir(videos_dir):
        media_info = MediaInfo.parse(videos_dir + f)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                f_after = __parse_filename(track.encoded_date) + '.' + f.split('.')[-1]
                __rename(videos_dir + f, videos_dir + f_after)


if __name__ == '__main__':
    main()
