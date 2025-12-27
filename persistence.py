   

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ore_data import OreDatabase


VARIANTS = {"normal", "ionized", "spectral"}


def _norm_variant(v: str | None) -> str:
    v = (v or "normal").strip().lower()
    return v if v in VARIANTS else "normal"


def _make_key(variant: str, ore_key: str) -> str:
                                                                            
    return f"{_norm_variant(variant)}|{ore_key}"


def _split_key(k: str) -> Tuple[str, str] | None:
    if "|" not in k:
        return None
    v, ok = k.split("|", 1)
    v = _norm_variant(v)
    if not ok:
        return None
    return v, ok


def load_state_from_obj(raw: Any, ore_db: OreDatabase) -> Tuple[str, str, Dict[str, bool], List[Dict[str, Any]]]:
       
    theme = "dark"
    variant = "normal"
    tracked: Dict[str, bool] = {}                                           
    logs: List[Dict[str, Any]] = []

                                                                     
    if isinstance(raw, dict) and "tracked_ores" in raw:
        settings = raw.get("settings") or {}
        t = (settings.get("theme") or "dark").strip().lower()
        theme = "light" if t == "light" else "dark"
        variant = _norm_variant(settings.get("variant"))
        raw_logs = raw.get("log") or raw.get("logs") or []
        if isinstance(raw_logs, list):
                                      
            logs = [e for e in raw_logs if isinstance(e, dict)]
        raw_tracked = raw.get("tracked_ores") or {}
        if not isinstance(raw_tracked, dict):
            return theme, variant, tracked, logs

        raw_map = {str(k): bool(v) for k, v in raw_tracked.items()}

                                                                           
        if any("|" in k for k in raw_map.keys()):
                                                              
            for k, v in raw_map.items():
                split = _split_key(k)
                if not split:
                    continue
                vv, ore_key = split
                tracked[_make_key(vv, ore_key)] = bool(v)
            return theme, variant, tracked, logs

                                                                                 
        all_ores = ore_db.get_all_ores()
        valid_ore_keys = {o.key for o in all_ores}
        for k, v in raw_map.items():
            if k in valid_ore_keys:
                tracked[_make_key("normal", k)] = bool(v)
            else:
                               
                for ore in all_ores:
                    if ore.name == k:
                        tracked[_make_key("normal", ore.key)] = bool(v)
        return theme, variant, tracked, logs

                                    
    if isinstance(raw, dict):
        name_map = {str(k): bool(v) for k, v in raw.items()}
                                                                                   
        for ore in ore_db.get_all_ores():
            if ore.name in name_map:
                tracked[_make_key("normal", ore.key)] = bool(name_map[ore.name])
        return theme, variant, tracked, logs

    return theme, variant, tracked, logs


def load_state(path: Path, ore_db: OreDatabase) -> Tuple[str, str, Dict[str, bool], List[Dict[str, Any]]]:
       
    if not path.exists():
        return "dark", "normal", {}, []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return "dark", "normal", {}, []

    return load_state_from_obj(raw, ore_db)


def save_state(
    path: Path,
    theme: str,
    variant: str,
    tracked_by_key: Dict[str, bool],
    ore_db: OreDatabase,
    logs: List[Dict[str, Any]] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    variant = _norm_variant(variant)
                                                                                                            
    valid_ore_keys = {o.key for o in ore_db.get_all_ores()}
    cleaned: Dict[str, bool] = {}
    for k, v in tracked_by_key.items():
        split = _split_key(str(k))
        if split:
            vv, ok = split
            if ok in valid_ore_keys and vv in VARIANTS:
                cleaned[_make_key(vv, ok)] = bool(v)
        else:
                                                            
            if str(k) in valid_ore_keys:
                cleaned[_make_key("normal", str(k))] = bool(v)
    tracked_by_key = cleaned
    data = {
        "settings": {"theme": "light" if str(theme).lower() == "light" else "dark", "variant": variant},
        "tracked_ores": {str(k): bool(v) for k, v in tracked_by_key.items()},
        "log": logs or [],
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


