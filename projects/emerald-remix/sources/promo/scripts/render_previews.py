#!/usr/bin/env python3
"""Current preview entry point. Round 4 renderer is retained in revisions/round4/."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('render_round5.py')),run_name='__main__')
