   

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


@dataclass(frozen=True)
class Asset:
    name: str
    download_url: str
    size: int | None = None


@dataclass(frozen=True)
class LatestRelease:
    tag_name: str
    html_url: str
    assets: list[Asset]


def is_frozen_exe() -> bool:
    return bool(getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS"))


def _version_tuple(v: str) -> tuple[int, int, int]:
       
    s = (v or "").strip()
    s = s[1:] if s.lower().startswith("v") else s
    parts = re.split(r"[^\d]+", s)
    nums = [int(p) for p in parts if p.isdigit()]
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])                              


def is_newer(latest_tag: str, current_version: str) -> bool:
    return _version_tuple(latest_tag) > _version_tuple(current_version)


def fetch_latest_release(repo: str, *, timeout_s: float = 10.0) -> LatestRelease:
    api = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(
        api,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "REx-R-Journal-Updater",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GitHub API error: HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e

    try:
        obj = json.loads(raw)
    except Exception as e:
        raise RuntimeError("Could not parse GitHub response.") from e

    tag = str(obj.get("tag_name") or "").strip()
    html = str(obj.get("html_url") or "").strip()
    assets_obj = obj.get("assets") or []
    assets: list[Asset] = []
    if isinstance(assets_obj, list):
        for a in assets_obj:
            if not isinstance(a, dict):
                continue
            name = str(a.get("name") or "")
            url = str(a.get("browser_download_url") or "")
            size = a.get("size")
            try:
                size_int = int(size) if size is not None else None
            except Exception:
                size_int = None
            if name and url:
                assets.append(Asset(name=name, download_url=url, size=size_int))

    if not tag:
        raise RuntimeError("GitHub latest release did not include a tag.")
    return LatestRelease(tag_name=tag, html_url=html, assets=assets)


def choose_windows_exe_asset(release: LatestRelease, preferred_name: str | None = None) -> Asset | None:
    assets = list(release.assets or [])
    if preferred_name:
        for a in assets:
            if a.name.lower() == preferred_name.lower():
                return a
                 
    exe_assets = [a for a in assets if a.name.lower().endswith(".exe")]
    if preferred_name:
        pref_lower = preferred_name.lower()
        for a in exe_assets:
            if a.name.lower() == pref_lower:
                return a
    if exe_assets:
                                                                           
        for a in exe_assets:
            if "helper" not in a.name.lower():
                return a
        return exe_assets[0]
    return None


def download_to_file(
    url: str,
    dest: Path,
    *,
    timeout_s: float = 30.0,
    progress_cb: Optional[Callable[[int], None]] = None,
    cancel_cb: Optional[Callable[[], bool]] = None,
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "REx-R-Journal-Updater"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        total = resp.headers.get("Content-Length")
        try:
            total_int = int(total) if total else None
        except Exception:
            total_int = None

        tmp = dest.with_suffix(dest.suffix + ".part")
        written = 0
        with open(tmp, "wb") as f:
            while True:
                if cancel_cb and cancel_cb():
                    raise RuntimeError("Download cancelled.")
                chunk = resp.read(1024 * 256)
                if not chunk:
                    break
                f.write(chunk)
                written += len(chunk)
                if progress_cb and total_int:
                    pct = int((written / total_int) * 100)
                    progress_cb(max(0, min(100, pct)))
        os.replace(tmp, dest)
        if progress_cb:
            progress_cb(100)


def make_helper_copy(current_exe: Path) -> Path:
       
    tmpdir = Path(tempfile.gettempdir())
    helper = tmpdir / f"{current_exe.stem}-updater{current_exe.suffix}"
    try:
        shutil.copy2(current_exe, helper)
    except Exception:
                           
        helper = tmpdir / f"{current_exe.stem}-updater-{os.getpid()}{current_exe.suffix}"
        shutil.copy2(current_exe, helper)
    return helper


def spawn_apply_update(helper_exe: Path, new_exe: Path, target_exe: Path) -> None:
       
    args = [str(helper_exe), "--apply-update", str(new_exe), str(target_exe)]
    kwargs: dict = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP                              
        kwargs["close_fds"] = True
    subprocess.Popen(args, **kwargs)


def apply_update_and_restart(new_exe: Path, target_exe: Path, *, wait_s: float = 60.0) -> None:
       
    new_exe = Path(new_exe)
    target_exe = Path(target_exe)
    start = time.time()

    backup = target_exe.with_suffix(target_exe.suffix + ".old")
    replaced = False

    while time.time() - start < wait_s:
        try:
                                                                                
            if target_exe.exists():
                try:
                    os.replace(target_exe, backup)
                except PermissionError:
                    time.sleep(0.5)
                    continue

            os.replace(new_exe, target_exe)
            replaced = True
            break
        except PermissionError:
            time.sleep(0.5)
            continue
        except Exception:
            time.sleep(0.5)
            continue

    if not replaced:
        raise RuntimeError("Timed out waiting to replace the executable (file may still be in use).")

                          
    try:
        subprocess.Popen([str(target_exe)], cwd=str(target_exe.parent))
    except Exception:
                                              
        pass

    if backup.exists():
        start2 = time.time()
        while time.time() - start2 < 3.0:
            try:
                backup.unlink(missing_ok=True)
                break
            except PermissionError:
                time.sleep(0.2)
            except Exception:
                break


