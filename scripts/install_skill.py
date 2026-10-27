#!/usr/bin/env python3
"""Install the bundled skill and bind it to this checkout's UI library."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', help='Default: CODEX_HOME or ~/.codex')
    parser.add_argument('--replace', action='store_true', help='Back up and replace an existing installation')
    args = parser.parse_args()
    home = Path(args.codex_home or os.getenv('CODEX_HOME') or Path.home() / '.codex').expanduser().resolve()
    source = PACKAGE_ROOT / 'skills/vocational-page-builder'
    library = PACKAGE_ROOT / 'high-school-ui'
    if not (source / 'SKILL.md').is_file() or not (library / 'data/library.json').is_file():
        parser.error('Keep the skill and high-school-ui together in the complete package.')
    parent = home / 'skills'
    target = parent / source.name
    if target.exists() and not args.replace:
        parser.error('Skill already exists; inspect it first, then use --replace to preserve a backup and replace it.')
    if target.is_symlink():
        parser.error('Refusing to replace a symlink; manage that installation explicitly.')
    parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='.vocational-install-', dir=parent) as temp:
        incoming = Path(temp) / source.name
        shutil.copytree(source, incoming, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        binding = incoming / 'references/library-binding.json'
        config = json.loads(binding.read_text(encoding='utf-8'))
        config['library_root'] = str(library)
        binding.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = home / 'skill-backups' / (source.name + '-' + stamp)
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
        try:
            incoming.rename(target)
        except OSError:
            if backup and not target.exists():
                backup.rename(target)
            raise
    print(json.dumps({'installed': str(target), 'library_root': str(library),
                      'backup': str(backup) if backup else None}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
