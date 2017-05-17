# -*- coding: utf-8 -*-
import traceback
from argparse import ArgumentParser
from enum import unique, Enum
from os import makedirs
from os.path import join, isdir
from subprocess import check_call
from xml.etree import ElementTree

from requests import HTTPError
from requests import Session


@unique
class Music(Enum):
    """NHK Gogaku music files list."""
    basic1 = 'english/basic1'
    basic2 = 'english/basic2'
    basic3 = 'english/basic3'
    kaiwa = 'english/kaiwa'
    timetrial = 'english/timetrial'
    kouryaku = 'english/kouryaku'
    business1 = 'english/business1'
    business2 = 'english/business2'
    yomu = 'english/yomu'
    enjoy = 'english/enjoy'
    chinese = 'chinese/kouza'
    chinese_levelup = 'chinese/levelup'
    hangeul = 'hangeul/kouza'
    hangeul_levelup = 'hangeul/levelup'
    italian = 'italian/kouza'
    german = 'german/kouza'
    french = 'french/kouza'
    spanish = 'spanish/kouza'
    russian = 'russian/kouza'


if __name__ == '__main__':

    # Read command options
    description = "'nhk-stream.py' downloads NHK Gogaku music files. "
    parser = ArgumentParser(description=description)
    parser.add_argument('music', type=str, nargs='+',
                        help='music file name. choose [{}]'.format(",".join([member.name for member in Music])))
    parser.add_argument('-f', '--force', action="store_true", help='overwrite files')
    parser.add_argument('-C', '--directory', type=str, default='',
                        help='change output directory (default: "%(default)s")')
    args = parser.parse_args()

    for name in args.music:
        if name not in [member.name for member in Music]:
            parser.error("Invalid sound file name [{}]".format(name))

    session = Session()

    try:
        # Get data list xml file
        musics = dict()
        for name in args.music:
            resp = session.get("https://cgi2.nhk.or.jp/gogaku/st/xml/{}/listdataflv.xml".format(Music[name].value))
            if resp.status_code != 200:
                raise HTTPError("Invalid URL [{}]".format(resp.url), response=resp)

            root = ElementTree.fromstring(resp.content.decode())
            musics[name] = [dict(title=e.get('title'), hdate=e.get('hdate'), kouza=e.get('kouza'), code=e.get('code'),
                                 file=e.get('file'), nendo=e.get('nendo'), pgcode=e.get('pgcode')) for e in root.iter('music')]

        # Execute ffmpeg
        for name, data_list in musics.items():

            # Make music files directory
            dir_name = join(args.directory, name)
            if not isdir(dir_name):
                makedirs(dir_name)

            for data in data_list:
                file = join(args.directory, name, "{}_{}_{}.mp3".format(data['title'], data['nendo'], data['hdate']))
                if isdir(file) and args.force:
                    continue
                url = "https://nhk-vh.akamaihd.net/i/gogaku-stream/mp4/{}/master.m3u8".format(data['file'])
                check_call(["ffmpeg", "-y", "-i", url, "-ab", "64k", "-id3v2_version", "3", file])

        exit(0)

    except Exception as e:
        print(traceback.format_exc())
        exit(1)
