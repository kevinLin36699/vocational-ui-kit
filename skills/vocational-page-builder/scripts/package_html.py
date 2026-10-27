#!/usr/bin/env python3
"""Inline a local classic-script HTML page into a new file; reject remote/module dependencies."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote


def attrs(text):
    return {m[1].lower(): m[3] for m in re.finditer(r'''([\w:-]+)\s*=\s*(["'])(.*?)\2''', text, re.S)}


def local(source, ref):
    parts = urlsplit(ref)
    if parts.scheme or parts.netloc or not parts.path:
        raise ValueError(f'Only local asset references supported: {ref}')
    path = (source.parent / unquote(parts.path)).resolve()
    try:
        path.relative_to(source.parent.resolve())
    except ValueError as exc:
        raise ValueError(f'Asset outside page directory: {ref}') from exc
    if not path.is_file():
        raise ValueError(f'Asset missing: {path}')
    return path


def package(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError(f'Refusing to overwrite {output}')
    text = source.read_text(encoding='utf-8')
    if re.search(r'<script\b[^>]*type\s*=\s*["\']module["\']', text, re.I):
        raise ValueError('Module scripts need the project build pipeline, not this inliner')
    def replace_link(match):
        a = attrs(match[0])
        if a.get('rel', '').lower() != 'stylesheet':
            return match[0]
        f = local(source, a.get('href', ''))
        css = f.read_text(encoding='utf-8')
        if re.search(r'@import\b|url\(', css, re.I):
            raise ValueError(f'CSS imports/media URLs need explicit asset packaging: {f}')
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        media = (' media="' + a['media'] + '"') if a.get('media') else ''
        return f'<style data-vpb-source="{f.relative_to(source.parent).as_posix()}" data-vpb-sha256="{digest}"{media}>\n{css}\n</style>'
    def replace_script(match):
        a = attrs(match[1])
        if not a.get('src'):
            return match[0]
        if a.get('type', '').lower() not in ('', 'text/javascript', 'application/javascript'):
            raise ValueError('Unsupported external script type')
        if re.search(r'\b(?:async|defer)\b', match[1], re.I):
            raise ValueError('Async/deferred script ordering needs a build-aware packager')
        f = local(source, a['src'])
        js = f.read_text(encoding='utf-8')
        if re.search(r'</script\s*>', js, re.I):
            raise ValueError('Script has a closing-script sequence; use a context-aware build pipeline')
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        return f'<script data-vpb-source="{f.relative_to(source.parent).as_posix()}" data-vpb-sha256="{digest}">\n{js}\n</script>'
    text = re.sub(r'<link\b[^>]*>', replace_link, text, flags=re.I)
    text = re.sub(r'<script\b([^>]*)>(.*?)</script\s*>', replace_script, text, flags=re.I | re.S)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding='utf-8')
    return {'output': str(output), 'bytes': output.stat().st_size, 'scope': 'local classic JS/CSS only; verify interactions after packaging'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        print(json.dumps(package(args.source, args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
