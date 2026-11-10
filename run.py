"""Reproduce the frozen analysis from official, SHA256-verified inputs."""
from pathlib import Path
import argparse, json, os, subprocess, sys, venv

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-env', action='store_true',
                        help='Use an existing environment with requirements.txt installed.')
    args = parser.parse_args()
    if args.current_env:
        python = Path(sys.executable)
    else:
        env_dir = ROOT / '.venv'
        python = env_dir / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(env_dir)
        subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                        '-r', str(ROOT / 'requirements.txt')], check=True, cwd=ROOT)
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    stages = [
        ['fetch_data.py'],
        ['analyze.py'],
        ['independent_check.py'],
        ['check_original.py', '--raw', 'raw/dice.csv', '--notebook',
         'sources/original_guardrail_notebook.ipynb', '--out', 'tables/audit'],
        ['plot_results.py'],
        ['build_report.py'],
    ]
    for stage in stages:
        print('RUN:', ' '.join(stage), flush=True)
        subprocess.run([str(python), *stage], check=True, cwd=ROOT, env=env)
    audit = json.loads((ROOT / 'tables/audit/audit_summary.json').read_text())
    assert audit['status'] == 'PASS' and audit['checks'] == 5032, audit
    print('PASS: official input hashes, fixed estimates, 5,032 independent checks, '
          'four original saved counts, figures and report.', flush=True)
    print('Raw inputs and participant-level outputs remain local and are gitignored.')

if __name__ == '__main__':
    main()
