#!/usr/bin/env python3
"""Create a new portable template seed, with exact-source provenance; no source mutation."""
import argparse
import html
import json
import shutil
import sys
from pathlib import Path
sys.dont_write_bytecode = True
from resolve_library import SKILL_ROOT, LibraryError, load_library, safe_path, sha256


def scaffold(output, pattern, title, library_root=None, version=None):
    lib = load_library(library_root, version)
    p = next((p for p in lib['patterns'] if p['id'] == pattern), None)
    if p is None:
        raise LibraryError(f'Unknown pattern: {pattern}')
    out = Path(output).expanduser().resolve()
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise LibraryError(f'Refusing to overwrite nonempty output: {out}')
    # Do not generate new task artifacts inside the source library or original business application.
    protected_roots = [lib['root']]
    if lib['binding'].get('source_project_root'):
        protected_roots.append(Path(lib['binding']['source_project_root']).resolve())
    for protected in protected_roots:
        if out == protected or protected in out.parents:
            raise LibraryError('Generate into an independent task directory; modify existing application in place manually')
    for relative in lib['assets']:
        safe_path(lib['root'], relative)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for relative in lib['assets']:
        src = safe_path(lib['root'], relative)
        dest_rel = 'assets/vocational-ui/' + relative
        dest = out / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        files.append({'source': relative, 'output': dest_rel, 'sha256': sha256(src)})
    shutil.copyfile(SKILL_ROOT / 'assets/page.css', out / 'page.css')
    provenance = {
        'schema_version': 1, 'skill': 'vocational-page-builder',
        'library_version': lib['manifest']['version'], 'library_root': str(lib['root']),
        'maturity': lib['manifest'].get('maturity'), 'pattern': pattern,
        'components': p['components'], 'data_mode': 'local-fictitious-demo',
        'seed_only': True, 'files': files, 'spec_hashes': lib['hashes']
    }
    styles = '\n'.join(f'<link rel="stylesheet" href="assets/vocational-ui/{html.escape(s, quote=True)}">' for s in lib['manifest']['styles'])
    scripts = '\n'.join(f'<script src="assets/vocational-ui/{html.escape(s, quote=True)}"></script>' for s in lib['manifest']['runtime'] + [lib['manifest']['patternsRuntime']])
    embedded = json.dumps(provenance, ensure_ascii=False).replace('<', '\\u003c')
    # Pattern identifiers have already been resolved from the library index; use JSON to encode JS values.
    pattern_literal = json.dumps(pattern, ensure_ascii=True).replace('<', '\\u003c')
    page = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
{styles}
<link rel="stylesheet" href="page.css">
</head>
<body>
<header class="vpb-banner"><span>{html.escape(title)}</span><span>组件库 v{html.escape(lib['manifest']['version'])} · 虚构演示数据 · 仅当前页面保留</span></header>
<main class="vpb-page"><div id="page"></div></main>
<script id="vpb-provenance" type="application/json">{embedded}</script>
{scripts}
<script>VocPatterns.mount(document.querySelector('#page'), {pattern_literal});</script>
</body></html>
'''
    (out / 'index.html').write_text(page, encoding='utf-8')
    (out / 'page-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'entry': str(out / 'index.html'), 'version': lib['manifest']['version'], 'pattern': pattern,
            'copied_assets': len(files), 'seed_only': True, 'note': 'Complete actual requirements; title does not replace fixed demo fields or data.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--pattern', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--library-root')
    parser.add_argument('--version')
    args = parser.parse_args()
    try:
        print(json.dumps(scaffold(args.output, args.pattern, args.title, args.library_root, args.version), ensure_ascii=False, indent=2))
    except (LibraryError, OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
