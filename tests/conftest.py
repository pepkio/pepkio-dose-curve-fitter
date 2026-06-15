"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "dose-curve-fitter",
        "title": "Dose-Response Curve Fitter",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "hts_batch_absolute",
                "description": "Three-compound HTS panel with absolute IC50",
                "input": {
                    "model": "auto",
                    "ic50_mode": "absolute",
                    "weighting": "none",
                    "compounds": [
                        {
                            "compound_id": "Drug-A",
                            "points": [
                                {"concentration_nM": 0.1, "response": 6},
                                {"concentration_nM": 1, "response": 8},
                                {"concentration_nM": 10, "response": 15},
                                {"concentration_nM": 100, "response": 45},
                                {"concentration_nM": 1000, "response": 78},
                                {"concentration_nM": 10000, "response": 91},
                                {"concentration_nM": 50000, "response": 94},
                                {"concentration_nM": 100000, "response": 95},
                            ],
                        },
                    ],
                },
                "output": {"has_blocking_errors": False},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "has_blocking_errors": False,
            "errors": [],
            "warnings": [],
            "compounds": [
                {
                    "compound_id": "Drug-A",
                    "qc_grade": "green",
                    "metrics": {"ic50_nM": 250.0, "pic50": 6.6},
                }
            ],
            "detected_unit": "nM",
            "audit_log": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
