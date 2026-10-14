#!/usr/bin/env python3
"""Build the unchanged Chaos package and reused scene-audio capture helper under shared admission.

Origin: Sonic3K Chaos reel revision, 2026-10-14. Maven, javac and the SDK
packager all inherit the same execution leases; no nested queue acquisition.
"""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

WT = Path(os.environ.get('OPENGGF_WORKTREE', Path.cwd())).resolve()
QUEUE_ROOT = Path(os.environ.get('OPENGGF_QUEUE_ROOT', '/home/farrell/code/projects/OpenGGF'))
sys.path.insert(0, str(QUEUE_ROOT / 'tools/testing'))
from maven_queue import handle_termination, inherited_slot, maven_slot


def main():
    with handle_termination():
        with maven_slot(WT, exclusive=True, estimate=75, kind='chaos-package-build') as leases:
            def run(command):
                child = subprocess.Popen(command, cwd=WT, start_new_session=True,
                                         **inherited_slot(leases))
                try:
                    status = child.wait()
                except BaseException:
                    os.killpg(child.pid, signal.SIGTERM)
                    try:
                        child.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        os.killpg(child.pid, signal.SIGKILL)
                        child.wait()
                    raise
                if status:
                    raise subprocess.CalledProcessError(status, command)

            run(['mvn', '-B', '-Dmse=off', '-DskipTests', 'test-compile', 'dependency:build-classpath',
                 '-Dmdep.outputFile=target/chaos-classpath.txt'])
            output = WT / 'target/sonic3k-chaos-mode'
            classes = output / 'classes'
            if classes.exists():
                shutil.rmtree(classes)
            classes.mkdir(parents=True)
            classpath = os.pathsep.join([str(WT / 'target/classes'),
                                        (WT / 'target/chaos-classpath.txt').read_text().strip()])
            project = WT / 'examples/sonic3k-chaos-mode'
            run(['javac', '--release', '25', '-cp', classpath, '-d', str(classes),
                 *map(str, sorted((project / 'src/main/java').rglob('*.java')))])
            shutil.copytree(project / 'src/main/resources', classes, dirs_exist_ok=True)
            jar = output / 'sonic3k-chaos-mode.jar'
            jar.unlink(missing_ok=True)
            run(['java', '--enable-native-access=ALL-UNNAMED', '-cp', classpath,
                 'com.openggf.tools.modsdk.GgfModCli', 'package', '--input', str(classes),
                 '--out', str(jar), '--warnings', 'error'])
            print(f'Built {jar}', flush=True)


if __name__ == '__main__':
    main()
