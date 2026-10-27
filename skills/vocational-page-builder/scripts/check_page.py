#!/usr/bin/env python3
"""Static/provenance validation only. Does not certify UI behavior or business correctness."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.references, self.ids, self.labels, self.duplicates = [], [], [], []
        self.inline, self.current, self.payload = [], None, ''

    def handle_starttag(self, tag, pairs):
        keys = [k for k, _ in pairs]
        a = dict(pairs)
        if len(keys) != len(set(keys)):
            self.duplicates.append(tag)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'label' and a.get('for'):
            self.labels.append(a['for'])
        if tag in ('script', 'link', 'img', 'source'):
            ref = a.get('href' if tag == 'link' else 'src')
            if ref:
                self.references.append((tag, ref, a))
        if tag in ('script', 'style'):
            self.current, self.payload = (tag, a), ''

    def handle_data(self, data):
        if self.current:
            self.payload += data

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')

    def handle_endtag(self, tag):
        if self.current and tag == self.current[0]:
            self.inline.append((self.current[0], self.current[1], self.payload))
            self.current, self.payload = None, ''


def check_page(entry):
    entry = Path(entry).resolve()
    parser = Page()
    parser.feed(entry.read_text(encoding='utf-8'))
    checks = []

    def record(name, ok, detail=''):
        checks.append(dict(name=name, status='passed' if ok else 'failed', detail=detail))

    record('No duplicate HTML attributes', not parser.duplicates, str(parser.duplicates))
    record('Unique static IDs', len(parser.ids) == len(set(parser.ids)))
    record('Explicit labels resolve', all(x in parser.ids for x in parser.labels))
    runtime_paths, referenced_paths = [], set()
    for tag, ref, attributes in parser.references:
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc:
            record('Local runtime resource ' + ref, False, 'External resource requires separate validation')
            continue
        f = (entry.parent / unquote(parts.path)).resolve()
        try:
            f.relative_to(entry.parent)
            contained = True
        except ValueError:
            contained = False
        record('Resource exists: ' + ref, contained and f.is_file())
        if contained and f.is_file():
            referenced_paths.add(f)
        if tag == 'script' and f.is_file():
            runtime_paths.append(f)
    provenance = [text for tag, a, text in parser.inline if a.get('id') == 'vpb-provenance']
    if not provenance:
        record('Page provenance', False, 'For existing applications, document reuse using their own project checks instead')
        return dict(entry=str(entry), checks=checks, limitation=__doc__)
    try:
        manifest = json.loads(provenance[0])
    except ValueError:
        record('Page provenance JSON', False)
        return dict(entry=str(entry), checks=checks, limitation=__doc__)
    record('Library version recorded', bool(re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][\w.-]+)?', str(manifest.get('library_version', '')))))
    bundle = {a['data-vpb-source']: (a, text) for tag, a, text in parser.inline if a.get('data-vpb-source')}
    seen = set()
    for asset in manifest.get('files', []):
        relative = asset['output']
        if relative in seen:
            record('Unique provenance asset ' + relative, False)
        seen.add(relative)
        if relative in bundle:
            a, text = bundle[relative]
            data = text.removeprefix('\n').removesuffix('\n').encode('utf-8')
            record('Inline source hash ' + relative, hashlib.sha256(data).hexdigest() == asset['sha256'] == a.get('data-vpb-sha256'))
        else:
            f = (entry.parent / relative).resolve()
            try:
                f.relative_to(entry.parent)
                ok = f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == asset['sha256']
            except ValueError:
                ok = False
            record('Copied source hash ' + relative, ok)
            record('Copied asset actually referenced ' + relative, f in referenced_paths)
    record('Nonempty asset provenance', bool(manifest.get('files')))
    sibling = entry.parent / 'page-provenance.json'
    if sibling.is_file() and not bundle:
        try:
            record('Embedded/sibling provenance agree', json.loads(sibling.read_text()) == manifest)
        except ValueError:
            record('Embedded/sibling provenance agree', False)
    node = shutil.which('node')
    if node:
        for f in runtime_paths:
            result = subprocess.run([node, '--check', str(f)], text=True, capture_output=True)
            record('JS syntax ' + f.name, result.returncode == 0, result.stderr[:300])
        with tempfile.TemporaryDirectory(prefix='vpb-inline-') as temp:
            for i, (tag, a, text) in enumerate(parser.inline):
                if tag != 'script' or a.get('src') or a.get('type', '') not in ('', 'text/javascript', 'application/javascript'):
                    continue
                f = Path(temp) / f'inline-{i}.js'
                f.write_text(text, encoding='utf-8')
                result = subprocess.run([node, '--check', str(f)], text=True, capture_output=True)
                record('Inline JS syntax ' + str(i), result.returncode == 0, result.stderr[:300])
    return dict(entry=str(entry), library_version=manifest.get('library_version'), pattern=manifest.get('pattern'),
                seed_only=manifest.get('seed_only'), checks=checks,
                not_checked=['business correctness', 'interactive behavior', 'visual fidelity', 'full accessibility'],
                node_available=bool(node), limitation=__doc__)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('entry')
    p.add_argument('--report')
    args = p.parse_args()
    try:
        report = check_page(args.entry)
        report['passed'] = all(c['status'] == 'passed' for c in report['checks'])
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.report:
            Path(args.report).write_text(text + '\n', encoding='utf-8')
        print(text)
        return 0 if report['passed'] else 1
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
