import json
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import create.config as config

README_TEMPLATE = """# {project_name}

Use `make` for build
"""

GITIGNORE_TEMPLATE = """build/
*.exe
*.o
*.obj
.vscode/
"""

def get_latest_archive_url():
    try:
        release = http_get_json(
            config.GITHUB_LATEST_RELEASE_API,
            headers=github_headers(accept="application/vnd.github+json"),
        )
    except (HTTPError, URLError, TimeoutError) as exc:
        tag = get_latest_tag_from_redirect()
        archive_name = archive_name_from_tag(tag)
        archive_url = f"https://github.com/{config.GITHUB_REPOSITORY}/releases/download/{tag}/{archive_name}"
        print(f"GitHub API unavailable ({exc}); using {archive_name}.")
        return archive_url, tag

    tag = release.get("tag_name", "latest")
    expected_archive_name = archive_name_from_tag(tag)

    for asset in release.get("assets", []):
        if asset.get("name") == expected_archive_name:
            return asset["browser_download_url"], tag

    for asset in release.get("assets", []):
        asset_name = asset.get("name", "")
        if re.fullmatch(r"InSDL-\d+\.\d+\.\d+\.zip", asset_name):
            return asset["browser_download_url"], tag

    raise ValueError(f"Release {tag} has no asset")

def archive_name_from_tag(tag):
    version = tag.removeprefix("v")
    return config.RELEASE_ARCHIVE_NAME.format(version=version)

def github_headers(accept=None):
    headers = {"User-Agent": "insdl-create"}
    if accept:
        headers["Accept"] = accept

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers

def http_get_json(url, headers=None):
    request = Request(url, headers=headers or {})
    with urlopen(request, timeout=config.DEFAULT_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))

def get_latest_tag_from_redirect():
    request = Request(config.GITHUB_LATEST_RELEASE_URL, headers=github_headers())
    with urlopen(request, timeout=config.DEFAULT_TIMEOUT) as response:
        match = re.search(r"/releases/tag/([^/?#]+)", response.url)
        if not match:
            raise ValueError(f"Cannot resolve latest release tag from {response.url}")
        return match.group(1)

def download_archive(url):
    request = Request(url, headers=github_headers())
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
        with urlopen(request, timeout=config.DEFAULT_TIMEOUT) as response:
            shutil.copyfileobj(response, tmp_file)
        return Path(tmp_file.name)

def _zip_root(names):
    clean_names = [name.replace("\\", "/") for name in names if name and not name.endswith("/")]
    roots = {name.split("/", 1)[0] for name in clean_names if "/" in name}
    root_files = [name for name in clean_names if "/" not in name]
    if len(roots) == 1 and not root_files:
        return next(iter(roots))
    return None

def extract_archive(archive_path, target_dir):
    target_dir = Path(target_dir).resolve()

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        members = zip_ref.infolist()
        root = _zip_root([member.filename for member in members])

        for member in members:
            member_name = member.filename.replace("\\", "/")
            if root and member_name.startswith(f"{root}/"):
                member_name = member_name[len(root) + 1:]
            if not member_name:
                continue

            destination = (target_dir / member_name).resolve()
            if target_dir not in destination.parents and destination != target_dir:
                raise ValueError(f"Unsafe archive path: {member.filename}")

            if member.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            with zip_ref.open(member, "r") as source, destination.open("wb") as output:
                shutil.copyfileobj(source, output)

def write_project_files(target_dir, project_name):
    readme_path = target_dir / "README.md"
    gitignore_path = target_dir / ".gitignore"

    readme_path.write_text(README_TEMPLATE.format(project_name=project_name), encoding="utf-8")
    gitignore_path.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")

def create_project(project_name):
    target_dir = (Path.cwd() / project_name).resolve()

    try:
        if target_dir.exists() and any(target_dir.iterdir()):
            print(f"Project '{project_name}' already exists and is not empty")
            return

        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Creating project '{project_name}'...")
        archive_url, release_tag = get_latest_archive_url()
        print(f"Downloading InSDL {release_tag}...")
        archive_path = download_archive(archive_url)

        try:
            extract_archive(archive_path, target_dir)
        finally:
            archive_path.unlink(missing_ok=True)

        write_project_files(target_dir, project_name)
        print(f"Project '{project_name}' created successfully in {target_dir}")

    except Exception as exc:
        print(f"Create error: {exc}")
