#!/usr/bin/env python3
"""Compatibility entry: python evals/control_contract.py --self-check"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from amc_guard import *  # noqa: F401,F403
from amc_guard import main

if __name__ == "__main__":
    raise SystemExit(main())
