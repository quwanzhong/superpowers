#!/usr/bin/env python3
import argparse
import fnmatch
import json
import os
import shutil
from pathlib import Path


def load_ignore_patterns(ignore_file: Path):
    patterns = []
    if ignore_file.exists():
        for line in ignore_file.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns


def is_ignored(rel_path: str, patterns):
    rel_path = rel_path.replace('\\', '/')
    for p in patterns:
        if fnmatch.fnmatch(rel_path, p):
            return True
    return False


def safe_read_text(path: Path):
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return None


def safe_write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def replace_in_file(path: Path, rel_path: str, replacements, ignore_patterns):
    if is_ignored(rel_path, ignore_patterns):
        return

    text = safe_read_text(path)
    if text is None:
        return

    new_text = text
    for k, v in replacements.items():
        new_text = new_text.replace(k, v)

    if new_text != text:
        safe_write_text(path, new_text)


def copy_template(template_dir: Path, target_dir: Path):
    if target_dir.exists() and any(target_dir.iterdir()):
        raise SystemExit(f"target_dir not empty: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    for src in template_dir.rglob('*'):
        rel = src.relative_to(template_dir)
        dst = target_dir / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def rename_package_path(target_dir: Path, package_name: str):
    pkg_path = package_name.replace('.', '/')
    src = target_dir / 'app' / 'src' / 'main' / 'java' / '__PACKAGE_PATH__'
    if src.exists():
        dst = target_dir / 'app' / 'src' / 'main' / 'java' / pkg_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            raise SystemExit(f"package path already exists: {dst}")
        shutil.move(str(src), str(dst))


def chmod_gradlew(target_dir: Path):
    gradlew = target_dir / 'gradlew'
    if gradlew.exists():
        try:
            mode = gradlew.stat().st_mode
            # add u+x
            gradlew.chmod(mode | 0o100)
        except Exception:
            # best-effort, do not fail generation
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_dir', required=True)
    parser.add_argument('--application_id', required=True)
    parser.add_argument('--package_name', required=True)
    parser.add_argument('--app_name', required=True)
    parser.add_argument('--base_url', required=True)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    template_dir = base_dir / 'template'
    config_file = base_dir / 'template.config.json'
    ignore_file = base_dir / 'template.ignore'

    if not template_dir.exists():
        raise SystemExit(f"template dir missing: {template_dir}")
    if not config_file.exists():
        raise SystemExit(f"config missing: {config_file}")

    config = json.loads(config_file.read_text(encoding='utf-8'))

    replacements = {
        '__APPLICATION_ID__': args.application_id,
        '__PACKAGE_NAME__': args.package_name,
        '__APP_NAME__': args.app_name,
        '__BASE_URL__': args.base_url,
    }

    ignore_patterns = load_ignore_patterns(ignore_file)

    target_dir = Path(args.target_dir).expanduser().resolve()

    copy_template(template_dir, target_dir)
    rename_package_path(target_dir, args.package_name)

    chmod_gradlew(target_dir)

    # Replace in text files
    for p in target_dir.rglob('*'):
        if p.is_dir():
            continue
        rel = p.relative_to(target_dir).as_posix()
        replace_in_file(p, rel, replacements, ignore_patterns)

    print('OK:', target_dir)


if __name__ == '__main__':
    main()
