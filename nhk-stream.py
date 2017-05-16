# -*- coding: utf-8 -*-
from enum import unique, Enum
from optparse import make_option, OptionParser

from requests import Session


@unique
class Sound(Enum):
    """NHK Gogaku sound files list."""
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
    usage = "usage: %prog [OPTION...] [SOUND...]"
    description = "'nhk-stream.py' downloads NHK Gogaku Sound files. " \
                  + "SOUND: {}".format(",".join([sound.name for sound in Sound]))
    options = [
        make_option('-f', '--force', action="store_true", dest='force',
                    help='overwrite files (default "%default")'),
        make_option('-C', '--directory', dest='directory', default='',
                    help='change directory (default "%default")'),
    ]
    options, args = OptionParser(usage, options, description=description).parse_args()

    if len(args) == 0:
        raise ValueError("nhk-stream.py: missing operand.\n"
                         + "Try 'nhk-stream.py --help' or 'nhk-stream.py --usage' for more information")

    for arg in args:
        if arg not in [sound.name for sound in Sound]:
            raise ValueError("Invalid sound file.\n"
                             + "Try 'nhk-stream.py --help' or 'nhk-stream.py --usage' for more information")

    # sound files, path,

    # Get data list xml file

    # Execute ffmpeg

    exit(0)
