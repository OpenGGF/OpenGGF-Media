#!/usr/bin/env python3
"""Author the revised Stageplay location comedy and its original dialogue decorations.
Inputs: a new output directory. Origin: OpenGGF Stageplay directing task, 2026-10-21.
No ROM bytes; panel PNGs are generated from the palette and geometry below.
"""
import argparse
import json
from pathlib import Path
import struct
import zlib


def key(f, x, y, a=5, **kw):
    return dict(frame=f, x=x, y=y, animation=a, **kw)


def cam(f, x, y):
    return dict(frame=f, x=x, y=y, zoom=1, interpolation='SMOOTH')


def line(start, end, who, text):
    return dict(startFrame=start, endFrame=end, speakerActor=who, text=text,
                skinId=who, typerId=who, x=12, y=12, width=376, height=64)


def title(start, end, text):
    return dict(startFrame=start, endFrame=end, text=text, x=35, y=18, argb=-256)


def sound(frame, sound_id, game='s2', kind='ROM_SFX'):
    return dict(frame=frame, kind=kind, gameId=game, soundId=sound_id)


def shake(start, end, ax=3, ay=2):
    return dict(startFrame=start, endFrame=end, amplitudeX=ax, amplitudeY=ay, frequency=9, seed=17)


def shot(id, frames, game, zone, act, camera, actors, dialogue, *, transition=None, audio=None, effects=None, captions=None):
    value = dict(id=id, durationFrames=frames, set=dict(gameId=game, zone=zone, act=act),
                 camera=camera, actors=actors, dialogue=dialogue, audio=audio or [],
                 cameraEffects=effects or [], captions=captions or [])
    if transition:
        value['transition'] = dict(kind=transition, durationFrames=30)
    return value


COLORS = {'sonic': 0xFF75BFFF, 'tails': 0xFFFFC65C, 'knuckles': 0xFFFF8282}


def screenplay():
    return dict(version=1, name='Location, Location, Location', width=400, height=224,
        dialogueTypers=[dict(id='sonic', framesPerGrapheme=1, punctuationPauseFrames=5),
                        dict(id='tails', framesPerGrapheme=2, punctuationPauseFrames=8),
                        dict(id='knuckles', framesPerGrapheme=3, punctuationPauseFrames=10)],
        dialogueSkins=[dict(id=who, nameArgb=color-(1 << 32), borderArgb=color-(1 << 32),
                           decorationAsset='decor/'+who+'.png', decorationBorder=5, padding=8)
                       for who, color in COLORS.items()],
        cast=[dict(id='sonic', name='Sonic', gameId='s2', character='sonic'),
              dict(id='tails', name='Tails', gameId='s2', character='tails'),
              dict(id='knuckles', name='Knuckles', gameId='s3k', character='knuckles')], shots=[
        shot('remote', 480, 's2', 0, 0, [cam(0, 0, 500), cam(420, 25, 500)], {
            'sonic': [key(0, -30, 655, 1), key(65, 150, 648), key(260, 150, 648, 8),
                      key(282, 150, 648, 2), key(318, 190, 590, 2), key(354, 220, 648, 8),
                      key(375, 220, 648)],
            'tails': [key(0, 330, 648, 0, flipX=True), key(60, 265, 648, flipX=True),
                      key(300, 265, 648, 7, flipX=True), key(350, 265, 648, 8, flipX=True),
                      key(388, 265, 648, flipX=True)]},
            [line(100, 265, 'tails', 'One button. Every location.'),
             line(285, 455, 'sonic', 'Great! Skip the walking.')],
            captions=[title(8, 86, 'LOCATION, LOCATION, LOCATION')],
            audio=[sound(0, 129, kind='ROM_MUSIC'), sound(282, 0xA0), sound(462, 0xA0)]),
        shot('closer', 360, 's2', 0, 0, [cam(0, 380, 470), cam(330, 410, 470)], {
            'sonic': [key(0, 485, 590, 2), key(28, 520, 622, 8), key(48, 520, 622),
                      key(140, 520, 622, 0), key(170, 560, 624, flipX=True), key(210, 560, 624)],
            'tails': [key(0, 610, 624, 8, flipX=True), key(50, 610, 624, 0),
                      key(80, 640, 624, flipX=True), key(280, 640, 624, 8, flipX=True)]},
            [line(45, 178, 'sonic', 'That was three steps.'),
             line(190, 330, 'tails', 'I was being careful.')], transition='WIPE_LEFT',
            audio=[sound(342, 0xA0)], effects=[shake(325, 350, 2, 2)]),
        shot('acttwo', 420, 's2', 0, 1, [cam(0, 0, 535), cam(360, 35, 535)], {
            'sonic': [key(0, 145, 560, 2), key(25, 145, 610, 2), key(46, 145, 687, 8),
                      key(65, 145, 687, 7), key(140, 145, 687, 0), key(192, 215, 687, flipX=True), key(232, 215, 687),
                      key(350, 215, 687, 8)],
            'tails': [key(0, 275, 545, 2, flipX=True), key(25, 275, 600, 2, flipX=True),
                      key(50, 275, 687, 8, flipX=True), key(72, 275, 687, flipX=True),
                      key(228, 275, 687, 0, flipX=True), key(260, 244, 687, flipX=True),
                      key(360, 244, 687, 8, flipX=True)]},
            [line(75, 215, 'sonic', 'Hang on... Act TWO?'),
             line(230, 392, 'tails', "Now you're getting it!")], transition='FADE_BLACK',
            audio=[sound(0, 129, kind='ROM_MUSIC'), sound(398, 0xA0)], effects=[shake(380, 410, 4, 2)]),
        shot('greenhill', 480, 's1', 0, 0, [cam(0, 0, 800), cam(390, 60, 800)], {
            'sonic': [key(0, -20, 944, 1), key(70, 190, 944, 7), key(215, 190, 944, 0, flipX=True),
                      key(245, 160, 944), key(340, 160, 944, 8),
                      key(385, 160, 944)],
            'tails': [key(0, 20, 944, 1), key(90, 295, 944, flipX=True), key(235, 295, 944, 0, flipX=True),
                      key(285, 245, 944, flipX=True), key(410, 245, 944, 8, flipX=True)]},
            [line(100, 245, 'sonic', 'I know this place!'),
             line(275, 445, 'tails', 'Oops. Wrong decade.')], transition='FADE_WHITE',
            audio=[sound(0, 129, 's1', 'ROM_MUSIC'), sound(462, 0xA0)], effects=[shake(440, 470, 3, 3)]),
        shot('island', 600, 's3k', 0, 0, [cam(0, 4900, 900), cam(180, 4950, 900), cam(560, 4910, 900)], {
            'sonic': [key(0, 5035, 930, 2), key(25, 5035, 985, 2), key(44, 5035, 1050, 8),
                      key(67, 5035, 1050), key(290, 5035, 1050, 0, flipX=True),
                      key(345, 4970, 1050), key(440, 4970, 1050, 8)],
            'tails': [key(0, 5110, 915, 2), key(25, 5110, 970, 2), key(48, 5110, 1052, 8),
                      key(75, 5110, 1052), key(245, 5110, 1052, 0, flipX=True),
                      key(305, 5050, 1052), key(440, 5050, 1052, 7), key(525, 5050, 1052, 8)],
            'knuckles': [key(0, 5290, 1046, 0, flipX=True), key(160, 5180, 1046, flipX=True),
                         key(260, 5180, 1046, 0, flipX=True), key(315, 5125, 1046, flipX=True),
                         key(500, 5125, 1046, 7, flipX=True)]},
            [line(85, 280, 'knuckles', 'This is a QUIET afternoon.'),
             line(295, 440, 'sonic', "We'll see ourselves out."),
             line(455, 575, 'tails', 'Found HOME!')], transition='WIPE_RIGHT',
            audio=[sound(0, 1, 's3k', 'ROM_MUSIC'), sound(44, 0xB1), sound(580, 0xA0)],
            effects=[shake(44, 75, 4, 3), shake(565, 592, 2, 2)]),
        shot('home', 420, 's2', 0, 0, [cam(0, 25, 500), cam(380, 0, 500)], {
            'sonic': [key(0, 170, 648, 0, flipX=True), key(65, 100, 650),
                      key(210, 100, 650, 0), key(245, 140, 648, 7), key(365, 140, 648, 8)],
            'tails': [key(0, 285, 648, 0, flipX=True), key(75, 235, 648, flipX=True),
                      key(275, 235, 648, 8, flipX=True), key(320, 235, 648, flipX=True)]},
            [line(90, 240, 'tails', 'Perfectly reliable!'),
             line(260, 385, 'sonic', 'Put. It. Down.')], transition='FADE_BLACK',
            audio=[sound(0, 129, kind='ROM_MUSIC'), sound(398, 0xA0)]),
        shot('mostly', 300, 's1', 0, 0, [cam(0, 20, 800), cam(280, 100, 800)], {
            'sonic': [key(0, 130, 944, 7), key(135, 130, 944, 1), key(295, 575, 944, 1)],
            'tails': [key(0, 240, 944, flipX=True), key(125, 240, 944, 1), key(240, 580, 944, 1)]},
            [line(30, 155, 'tails', '...Mostly.')], transition='FADE_WHITE',
            captions=[title(190, 299, 'OpenGGF Stageplay\nDirect the unexpected.')],
            audio=[sound(0, 129, 's1', 'ROM_MUSIC')])])


def panel_png(color):
    """20px original nine-slice panel; 5px corners, opaque middle, no ROM art."""
    pixels = []
    rgb = ((color >> 16) & 255, (color >> 8) & 255, color & 255)
    for y in range(20):
        row = bytearray([0])
        for x in range(20):
            edge = min(x, y, 19-x, 19-y)
            if edge == 0: c = (8, 12, 20, 255)
            elif edge == 1: c = (*rgb, 255)
            elif edge == 2: c = tuple(int(v*.42) for v in rgb)+(255,)
            else: c = (16, 24, 39, 255)
            row.extend(c)
        pixels.append(row)
    def chunk(kind, data):
        return struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data)&0xFFFFFFFF)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB',20,20,8,6,0,0,0))+chunk(b'IDAT', zlib.compress(b''.join(pixels)))+chunk(b'IEND',b'')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_dir',type=Path)
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'decor').mkdir()
    for who,color in COLORS.items():
        (args.output_dir/'decor'/f'{who}.png').write_bytes(panel_png(color))
    with (args.output_dir/'location-remote.screenplay.json').open('x') as stream:
        json.dump(screenplay(),stream,indent=2)
        stream.write('\n')
