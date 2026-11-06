# Pepkio Dose-Response Curve Fitter

Call the Pepkio dose-curve-fitter REST API from Python to batch-fit 4PL/5PL curves and return IC50, pIC50, and QC grades per compound.

# What It Does

HTS and pharmacology pipelines need IC50, EC50, pIC50, and Hill slope for many compounds at once. Rebuilding logistic regression and per-compound QC in a notebook for each screen is slow and inconsistent.

This package submits concentration–response data (CSV text or structured `compounds` arrays) to the same Pepkio Tools engine as the hosted web calculator. It returns fitted model parameters, per-compound metrics, green/amber/red QC grades with plain-English messages, and shareable run permalinks.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Models: `four_pl`, `five_pl`, or `auto` (F-test selects best)
- IC50 modes: relative (Top=100, Bottom=0) or absolute with optional `constraints`
- Weighting: `none`, `1/y`, or `1/y2`
- Per-compound metrics: IC50, EC50, pIC50, EC10, EC90, Hill slope, R²
- QC grades with plain-English `qc_messages`
- CSV input via `csv_text` (`compound_id`, `concentration`, `response`)
- Manifest examples: `hts_batch_absolute`, `relative_ic50`, `flat_line_failure`, `few_points_blocking`
- CLI: `pepkio-dose-curve-fitter manifest` and `run`
- Configuration via `PEPKIO_API_KEY`, `LOCAL_PEPKIO_API_KEY`, and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-dose-curve-fitter
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_dose_curve_fitter import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("hts_batch_absolute")
    result = client.run(inp)
    for compound in result.result["compounds"]:
        m = compound["metrics"]
        print(compound["compound_id"], m["ic50_nM"], m["pIC50"], compound["qc_grade"])
```

CLI:

```bash
pepkio-dose-curve-fitter run --example hts_batch_absolute
```

Manifest inspection does not require an API key.

# Typical Use Cases

- Batch IC50 fitting from a multi-compound HTS CSV
- Kinase inhibitor panel potency with pIC50 for SAR tables
- Comparing `auto` vs forced 4PL/5PL model selection
- QC screening for flat responses or too few dose points before reporting
- Automated reanalysis of dose-response exports in notebooks or CI

# Scientific Background

4PL and 5PL logistic models fit sigmoidal concentration–response data. IC50 is the inflection concentration; pIC50 is −log10(IC50). Relative mode fixes Top=100 and Bottom=0; absolute mode estimates plateaus from data. Zero concentration points are excluded. Fewer than four points per compound returns blocking errors.

# Web Application

For researchers who prefer a graphical interface, an interactive [Dose-Response Curve Fitter](https://www.pepkio.com/tools/dose-curve-fitter) is available in the browser.

The web interface adds per-compound curve review, outlier exclusion, bootstrap CI for IC50, SVG/PDF figure export, methods PDF, shareable links, and reload of recent runs.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-dose-curve-fitter](https://github.com/pepkio/pepkio-dose-curve-fitter)

Web application: [https://www.pepkio.com/tools/dose-curve-fitter](https://www.pepkio.com/tools/dose-curve-fitter)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

dose-response fitter, IC50 API, EC50 calculator, pIC50, 4PL 5PL, HTS batch fitting, Hill slope, pharmacology Python, pepkio-dose-curve-fitter, REST API curve fit, kinase panel IC50, SAR potency, sigmoidal regression, relative absolute IC50, QC grade dose-response, CSV compound screen, how to fit IC50 from Python HTS data, batch pIC50 SAR table programmatically, auto select 4PL or 5PL via API, flag flat dose-response before reporting IC50, run dose-response fit in CI pipeline Pepkio, compare relative vs absolute IC50 script, EC10 EC90 from logistic fit Python client

A semantic, AI-native version of this document in the K2F format is available at https://k2f.dev (https://k2f.dev/v/eb424a331d64e9e82a6e9bcb6bfdaf23cabeff15fed9cad3fb01bb026aa02233)
