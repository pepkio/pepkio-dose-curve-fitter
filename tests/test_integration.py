"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_dose_curve_fitter.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "dose-curve-fitter"
    names = live_client.list_examples()
    assert "hts_batch_absolute" in names


def test_run_hts_batch_absolute(live_client: PepkioClient):
    inp = live_client.get_example_input("hts_batch_absolute")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    compounds = result.result.get("compounds")
    assert isinstance(compounds, list)
    assert len(compounds) == 3
    drug_a = next(c for c in compounds if c.get("compound_id") == "Drug-A")
    assert drug_a.get("metrics", {}).get("ic50_nM", 0) > 0
    assert drug_a.get("qc_grade") == "green"
    assert result.error is None


def test_run_relative_ic50(live_client: PepkioClient):
    inp = live_client.get_example_input("relative_ic50")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    compounds = result.result.get("compounds")
    assert isinstance(compounds, list)
    assert len(compounds) >= 1


def test_run_few_points_blocking(live_client: PepkioClient):
    inp = live_client.get_example_input("few_points_blocking")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is True
