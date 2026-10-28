#!/usr/bin/env python3
"""Exercise the downloadable package, binding overrides and installer in temporary folders."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    checks = []

    def check(name, condition):
        checks.append({'name': name, 'status': 'passed' if condition else 'failed'})
        if not condition:
            raise AssertionError(name)

    with tempfile.TemporaryDirectory(prefix='vocational-distribution-') as temp:
        work = Path(temp).resolve()
        checkout = work / 'moved-checkout'
        for name in ['high-school-ui', 'skills', 'scripts']:
            shutil.copytree(ROOT / name, checkout / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        skill = checkout / 'skills/vocational-page-builder'
        resolver = skill / 'scripts/resolve_library.py'
        env = {k: v for k, v in os.environ.items() if k != 'VOCATIONAL_UI_LIBRARY_ROOT'}

        def run(script, *args, cwd=work, extra_env=None):
            return subprocess.run([sys.executable, str(script), *map(str, args)],
                                  cwd=cwd, env={**env, **(extra_env or {})},
                                  capture_output=True, text=True)

        result = run(resolver, '--component', 'table', '--component', 'form',
                     '--component', 'application-tracker', '--component', 'asset-loan')
        check('Relocated checkout resolves from an unrelated working directory', result.returncode == 0)
        info = json.loads(result.stdout)
        check('Current version and all component families resolve',
              info['version'] == '2.7.1' and info['counts']['components'] == 118
              and len(info['components']) == 4 and not info['changed_files'])
        check('All declared documents, contracts and examples exist',
              all(Path(p).is_file() for group in ['documents', 'contracts', 'examples']
                  for p in info[group].values()))
        check('Business and configurable-control standards are discoverable',
              {'controls', 'table_form', 'education', 'education_next',
               'education_platform', 'business_examples'} <= info['documents'].keys()
              and 'controls' in info['contracts'])
        check('Requested version mismatch is refused', run(resolver, '--version', '2.0.0').returncode == 2)
        other = ROOT / 'high-school-ui'
        explicit = run(resolver, '--library-root', other)
        environment = run(resolver, extra_env={'VOCATIONAL_UI_LIBRARY_ROOT': str(other)})
        project = work / 'project'
        project.mkdir()
        (project / '.vocational-page-builder.json').write_text(json.dumps({
            'library_root': '../moved-checkout/high-school-ui'}))
        configured = run(resolver, cwd=project)
        check('Explicit, environment and project-relative overrides resolve',
              all(p.returncode == 0 for p in [explicit, environment, configured])
              and json.loads(explicit.stdout)['resolved_from'] == 'explicit'
              and json.loads(environment.stdout)['resolved_from'] == 'environment'
              and Path(json.loads(configured.stdout)['library_root']) == checkout / 'high-school-ui')
        page = work / 'generated-page'
        seed = run(skill / 'scripts/scaffold_page.py', '--output', page,
                   '--pattern', 'list', '--title', '设备借还管理')
        check('Scaffold works without original business source', seed.returncode == 0)
        provenance = json.loads((page / 'page-provenance.json').read_text())
        manifest = json.loads((checkout / 'high-school-ui/data/library.json').read_text())
        expected = set(manifest['styles'] + manifest['runtime'] + [manifest['patternsRuntime']])
        check('All current runtime assets are copied without showcase fixtures',
              {item['source'] for item in provenance['files']} == expected
              and not expected.intersection(manifest['showcaseRuntime']))
        page_check = run(skill / 'scripts/check_page.py', page / 'index.html')
        report = json.loads(page_check.stdout)
        check('Scaffold references, syntax and provenance hashes pass',
              page_check.returncode == 0 and all(c['status'] == 'passed' for c in report['checks']))
        installer = checkout / 'scripts/install_skill.py'
        codex = work / 'codex-home'
        installed = codex / 'skills/vocational-page-builder'
        first = run(installer, '--codex-home', codex)
        check('Installer binds to the downloaded checkout',
              first.returncode == 0 and json.loads((installed / 'references/library-binding.json').read_text())['library_root']
              == str(checkout / 'high-school-ui'))
        check('Installer refuses accidental replacement', run(installer, '--codex-home', codex).returncode != 0)
        old_skill = (installed / 'SKILL.md').read_bytes()
        replaced = run(installer, '--codex-home', codex, '--replace', '--library-root', other)
        details = json.loads(replaced.stdout)
        check('Explicit binding replacement preserves a recoverable backup',
              replaced.returncode == 0 and (Path(details['backup']) / 'SKILL.md').read_bytes() == old_skill
              and details['library_root'] == str(other))
        check('Installed skill resolves its actual bound library',
              run(installed / 'scripts/resolve_library.py').returncode == 0)
    report = {'library_version': '2.7.1', 'skill_version': '1.2.0', 'checks': checks,
              'passed': len(checks), 'failed': 0,
              'scope': 'Package portability, binding, installer and static scaffold; no browser or production-service assertion.'}
    (ROOT / 'distribution-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
