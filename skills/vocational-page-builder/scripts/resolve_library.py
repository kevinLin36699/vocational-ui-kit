#!/usr/bin/env python3
"""Read the current bound UI library. Standard library only; never writes to it."""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
BINDING = SKILL_ROOT / 'references/library-binding.json'


class LibraryError(ValueError):
    pass


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise LibraryError(f'Cannot read JSON {path}: {exc}') from exc


def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise LibraryError(f'Expected library-relative file path: {relative!r}')
    p = (root / relative).resolve()
    try:
        p.relative_to(root.resolve())
    except ValueError as exc:
        raise LibraryError(f'Path escapes library root: {relative}') from exc
    if not p.is_file():
        raise LibraryError(f'Required library file missing: {p}')
    return p


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semver(version):
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?', str(version))
    if not match:
        raise LibraryError(f'Invalid semantic version: {version!r}')
    return tuple(int(x) for x in match.groups())


def load_library(library_root=None, version=None):
    binding = read_json(BINDING)
    origin = 'explicit' if library_root else 'environment' if os.getenv('VOCATIONAL_UI_LIBRARY_ROOT') else 'binding'
    chosen = library_root or os.getenv('VOCATIONAL_UI_LIBRARY_ROOT')
    if not chosen:
        for parent in [Path.cwd(), *Path.cwd().parents]:
            cfg = parent / '.vocational-page-builder.json'
            if cfg.is_file():
                project = read_json(cfg)
                chosen = project.get('library_root')
                if not isinstance(chosen, str) or not chosen:
                    raise LibraryError(f'{cfg} requires nonempty library_root')
                if not Path(chosen).is_absolute():
                    chosen = str(parent / chosen)
                origin = str(cfg)
                break
    # Distribution bindings are relative to the skill folder; explicit/project overrides retain their own context.
    candidate = Path(chosen or binding['library_root']).expanduser()
    if not chosen and not candidate.is_absolute():
        candidate = SKILL_ROOT / candidate
    root = candidate.resolve()
    source_root = binding.get('source_project_root')
    if source_root:
        source_path = Path(source_root).expanduser()
        binding['source_project_root'] = str((SKILL_ROOT / source_path).resolve() if not source_path.is_absolute() else source_path.resolve())
    manifest_path = safe_path(root, binding['manifest'])
    meta = read_json(manifest_path)
    actual = str(meta.get('version', ''))
    current, baseline = semver(actual), semver(binding['baseline_version'])
    if version and actual != version:
        raise LibraryError(f'Requested version {version}, available {actual}; no silent downgrade')
    policy = binding.get('version_policy', 'compatible-major')
    if policy == 'pinned' and actual != binding['baseline_version']:
        raise LibraryError('Pinned library version changed; inspect and explicitly update the binding')
    if policy not in ('pinned', 'compatible-major'):
        raise LibraryError(f'Unknown version_policy: {policy}')
    if current[0] != baseline[0]:
        raise LibraryError(f'Library major version changed ({actual}); inspect new API before updating baseline_version')
    index_paths = {k: safe_path(root, meta[k]) for k in ('componentIndex', 'tokenIndex', 'pagePatternIndex', 'generationStandard')}
    components = read_json(index_paths['componentIndex'])
    tokens = read_json(index_paths['tokenIndex'])
    patterns = read_json(index_paths['pagePatternIndex'])
    if not isinstance(components, list) or not isinstance(patterns, list) or not isinstance(tokens, dict):
        raise LibraryError('Unsupported component/token/pattern index schema')
    for label, items, key in [('component', components, 'key'), ('pattern', patterns, 'id')]:
        ids = [x.get(key) for x in items]
        if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
            raise LibraryError(f'Invalid or duplicate {label} identifiers')
        if any(str(x.get('version', actual)) != actual for x in items):
            raise LibraryError(f'{label} index version differs from manifest')
    if str(tokens.get('version')) != actual:
        raise LibraryError('Token version differs from manifest')
    for label, key, items in [('components', 'components', components), ('pagePatterns', 'pagePatterns', patterns), ('tokens', 'tokens', tokens.get('tokens', {}))]:
        if meta.get(key) != len(items):
            raise LibraryError(f'Manifest {label} count does not match index')
    styles, runtime = meta.get('styles'), meta.get('runtime')
    if not isinstance(styles, list) or not isinstance(runtime, list) or not styles or not runtime:
        raise LibraryError('Manifest styles/runtime must be nonempty lists')
    assets = list(dict.fromkeys(styles + runtime + [meta['patternsRuntime']]))
    for name in assets:
        safe_path(root, name)
    documents = {k: str(safe_path(root, path)) for k, path in binding['documents'].items()}
    documents['generation_standard'] = str(index_paths['generationStandard'])
    # Resolve current conditional standards from the library manifest, not copied skill rules.
    for key, field in {'resource_composer': 'resourceComposerStandard', 'skill_selection': 'skillSelectionStandard',
                       'teaching_agents': 'teachingAgentStandard', 'generated_content': 'generatedContentStandard'}.items():
        if meta.get(field):
            documents[key] = str(safe_path(root, meta[field]))
    contracts = {key: str(safe_path(root, meta[field])) for key, field in {
        'resource_composer': 'resourceComposerContract', 'skill_selection': 'skillSelectionContract',
        'teaching_agents': 'teachingAgentContract', 'workspace': 'workspaceContract',
        'message_feedback': 'messageFeedbackContract'}.items() if meta.get(field)}
    examples = {key: str(safe_path(root, path)) for key, path in binding.get('examples', {}).items()}
    tracked = [binding['manifest'], *[str(p.relative_to(root)) for p in index_paths.values()], *assets,
               *[str(Path(p).relative_to(root)) for p in documents.values()]]
    tracked += [str(Path(p).relative_to(root)) for p in [*contracts.values(), *examples.values()]]
    hashes = {p: sha256(safe_path(root, p)) for p in dict.fromkeys(tracked)}
    baseline_hashes = binding.get('baseline_hashes', {})
    changed = [p for p, digest in hashes.items() if baseline_hashes.get(p) and baseline_hashes[p] != digest]
    notes = []
    if actual != binding['baseline_version']:
        notes.append('Compatible version differs from baseline; read current API/specs before generating.')
    if changed:
        notes.append('Tracked files changed; source is authoritative. Re-read changed files and revalidate needed behavior.')
    return dict(root=root, binding=binding, origin=origin, manifest=meta, components=components,
                tokens=tokens, patterns=patterns, assets=assets, documents=documents,
                hashes=hashes, changed=changed, notes=notes, contracts=contracts, examples=examples)


def describe(lib, component_keys=(), pattern_keys=()):
    comps = {x['key']: x for x in lib['components']}
    patterns = {x['id']: x for x in lib['patterns']}
    missing = (set(component_keys) - set(comps)) | (set(pattern_keys) - set(patterns))
    if missing:
        raise LibraryError('Unknown component or pattern: ' + ', '.join(sorted(missing)))
    return {
        'library_root': str(lib['root']), 'resolved_from': lib['origin'],
        'version': lib['manifest']['version'], 'maturity': lib['manifest'].get('maturity'),
        'counts': {k: lib['manifest'][k] for k in ('components', 'pagePatterns', 'tokens')},
        'documents': lib['documents'], 'contracts': lib['contracts'], 'examples': lib['examples'],
        'preview_only_examples': lib['binding'].get('preview_only_examples', []), 'assets': lib['assets'],
        'index_paths': {k: str(lib['root'] / lib['manifest'][k]) for k in ('componentIndex', 'tokenIndex', 'pagePatternIndex')},
        'source_project_root': lib['binding'].get('source_project_root'),
        'components': [comps[k] for k in component_keys], 'patterns': [patterns[k] for k in pattern_keys],
        'changed_files': lib['changed'], 'notes': lib['notes'], 'hashes': lib['hashes']
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library-root')
    parser.add_argument('--version')
    parser.add_argument('--component', action='append', default=[])
    parser.add_argument('--pattern', action='append', default=[])
    args = parser.parse_args()
    try:
        lib = load_library(args.library_root, args.version)
        print(json.dumps(describe(lib, args.component, args.pattern), ensure_ascii=False, indent=2))
    except (LibraryError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
