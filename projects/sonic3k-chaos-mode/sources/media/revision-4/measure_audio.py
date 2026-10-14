#!/usr/bin/env python3
"""Measure native source/mix loudness for the 2026-10-14 Chaos reel revision 4.
Inputs are native HCZ2 and observed-event SFX WAVs; no PCM edits or Java work.
All FFmpeg children inherit the normal shared admission/worktree lease.
"""
import argparse
import json
from pathlib import Path
import assemble


def measure(path, audio_filter):
    child = assemble.launch(['ffmpeg', '-nostdin', '-hide_banner', '-v', 'info',
        '-threads', '1', '-i', str(path), '-vn', '-af', audio_filter +
        ',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
        stdout=assemble.subprocess.PIPE, stderr=assemble.subprocess.PIPE)
    try:
        _, error = child.communicate()
        if child.returncode:
            raise RuntimeError(error.decode(errors='replace')[-2000:])
        text = error.decode()
        return json.loads(text[text.rfind('{'):text.rfind('}')+1])
    finally:
        assemble.stop(child)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--admission-worktree', type=Path, required=True)
    a = p.parse_args()
    with assemble.admitted(a.admission_worktree, estimate=15):
        result = {
            'bed': measure(assemble.ROOT/'assets/hcz2/native-hcz2.wav', 'atrim=end=106'),
            'selected_ghost_sfx': measure(assemble.ROOT/'assets/ghosts/native-sfx.wav',
                'atrim=start_sample=441600:end_sample=715200,asetpts=PTS-STARTPTS'),
            'purpose': 'Source measurement only; mixer gains and final AAC are verified separately.'}
        (assemble.ROOT/'out/audio-source-levels.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result))

if __name__ == '__main__':
    main()
