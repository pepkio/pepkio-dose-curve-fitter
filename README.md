# Pepkio Dose-Response Curve Fitter

Fit IC50 and EC50 for every compound in a dose-response screen from one CSV upload.

# Overview

High-throughput screening (HTS) and pharmacology workflows produce concentration–response data for many compounds at once. Each compound needs a sigmoidal curve fit to estimate potency metrics such as IC50 (half-maximal inhibitory concentration), EC50 (half-maximal effective concentration), Hill slope, pIC50, EC10, and EC90. In practice, researchers export plate-reader or assay data, then fit curves one compound at a time in desktop software or rebuild logistic regression in spreadsheets—slow steps where unreliable plateaus, flat responses, or too few dose points are easy to miss until SAR tables or manuscripts are drafted.

The Pepkio Dose-Response Curve Fitter (tool ID: `dose-curve-fitter`) accepts multi-compound concentration–response data from a CSV upload or structured JSON input. It fits four-parameter logistic (4PL) or five-parameter logistic (5PL) models per compound, can select the better model automatically via F-test (`auto` mode), and reports IC50, Hill slope, R², pIC50, EC10, and EC90 with a per-compound fit-quality grade. Relative IC50 mode fixes Top=100 and Bottom=0; absolute IC50 mode estimates free top and bottom plateaus with optional constraints.

Researchers use dose-response curve fitters for HTS and dose-response screens, kinase and receptor inhibitor panels, SAR tables needing pIC50 values, teaching pharmacology, and sharing analyses with collaborators. This repository provides a Python client and CLI for the same calculation engine used by the hosted web application at [https://www.pepkio.com/tools/dose-curve-fitter](https://www.pepkio.com/tools/dose-curve-fitter).

# Features

- **Batch fitting:** Fit every compound in a screen from one CSV or `compounds` array instead of one curve at a time
- **Curve models:** `four_pl`, `five_pl`, or `auto` (F-test selects the better model)
- **IC50 modes:** Relative (Top=100, Bottom=0) or absolute (free Top/Bottom with optional `constraints`)
- **Regression weighting:** `none`, `1/y`, or `1/y2`
- **Concentration units:** Internal nM; optional `concentration_unit` display hint (e.g. nM, µM)
- **Per-compound metrics:** IC50, EC50, pIC50, EC10, EC90, Hill slope, R²
- **QC grades:** Green, amber, or red with plain-English `qc_messages` per compound
- **CSV input:** Optional `csv_text` with `compound_id`, `concentration`, `response` columns
- **Zero concentration exclusion:** Points at zero concentration are excluded from fitting
- **Structured output:** `compounds` array with fit parameters, residuals, metrics, and audit log
- **Manifest examples:** `hts_batch_absolute`, `relative_ic50`, `flat_line_failure`, `few_points_blocking`
- **Python API and CLI:** `PepkioClient`, `get_manifest`, `get_example_input`, `run`, `get_run`
- **Shareable runs:** API returns `permalink` URLs for each completed run

The hosted web version adds interactive curve review per compound, outlier exclusion, bootstrap confidence intervals for IC50 on demand, SVG or PDF figure export, CSV download of all results, methods PDF for manuscripts, shareable links to reopen analyses, and browser storage of recent runs.

# Common Use Cases

- **HTS dose-response screens:** Upload a multi-compound CSV from a plate reader and obtain IC50 values for an entire panel in one step
- **Kinase inhibitor panels:** Compare potency across inhibitors with pIC50 values for SAR tables
- **Receptor agonist/antagonist assays:** Fit EC50 and EC90 alongside IC50 for pharmacology reporting
- **Model selection:** Let `auto` choose between 4PL and 5PL, or force a specific model for consistency across a study
- **Relative vs absolute IC50:** Use relative mode when normalizing to 0–100% response, or absolute mode when top and bottom plateaus must be estimated from data
- **QC before reporting:** Review green/amber/red grades and plain-English warnings before adding IC50 values to a lab notebook or publication
- **Teaching pharmacology:** Demonstrate dose-response fitting without a paid desktop license
- **Scripted reanalysis:** Re-run the same fitting logic from notebooks, LIMS hooks, or CI via the Python client

# Why This Tool Exists

Spreadsheets lack built-in four-parameter logistic regression and batch QC for dozens of compounds. GraphPad Prism fits dose–response curves well but typically processes one compound at a time and requires a paid license. Free web calculators often handle a single curve without batch mode or fit-quality checks. R packages such as `drc` automate batch fitting but require scripting and environment setup.

The dose-curve-fitter tool accepts a multi-compound CSV, grades every fit with plain-English warnings, can pick between 4PL and 5PL automatically, and returns structured JSON for downstream tables. The Python client runs the same engine from scripts or pipelines via the Pepkio Tools REST API.

# Installation

```bash
pip install pepkio-dose-curve-fitter
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-dose-curve-fitter
```

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |

Manifest inspection does not require an API key.

# Quick Start

### Python

```python
from pepkio_dose_curve_fitter import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("hts_batch_absolute")
    result = client.run(inp)
    print(result.status, result.permalink)
    for compound in result.result["compounds"]:
        m = compound["metrics"]
        print(
            compound["compound_id"],
            f"IC50={m['ic50_nM']:.1f} nM",
            f"pIC50={m['pIC50']:.2f}",
            compound["qc_grade"],
        )
```

### CLI

```bash
# Manifest (no API key)
pepkio-dose-curve-fitter manifest
pepkio-dose-curve-fitter manifest --examples

# Run a named example (API key required)
pepkio-dose-curve-fitter run --example hts_batch_absolute
pepkio-dose-curve-fitter run --example relative_ic50

# Run custom JSON input
pepkio-dose-curve-fitter run --input-json '{"model":"four_pl","ic50_mode":"absolute","compounds":[]}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

Running the `hts_batch_absolute` manifest example against the production API returns:

```json
{
  "status": "completed",
  "run_id": "30601204-dccd-4c65-88c1-54593a46b85f",
  "permalink": "https://tools.pepkio.com/r/30601204-dccd-4c65-88c1-54593a46b85f",
  "result": {
    "has_blocking_errors": false,
    "compounds": [
      {
        "compound_id": "Drug-A",
        "metrics": {
          "ic50_nM": 142.17,
          "ec50_nM": 142.17,
          "pIC50": 6.85,
          "ec10_nM": 7.84,
          "ec90_nM": 2578.72,
          "hill_slope": 0.758
        },
        "qc_grade": "green",
        "fit": { "model": "four_pl", "r_squared": 0.9998 }
      },
      {
        "compound_id": "Drug-B",
        "metrics": {
          "ic50_nM": 404.01,
          "ec50_nM": 404.01,
          "pIC50": 6.39,
          "ec10_nM": 11.46,
          "ec90_nM": 14243.78,
          "hill_slope": 0.617
        },
        "qc_grade": "green",
        "fit": { "model": "four_pl", "r_squared": 0.9994 }
      },
      {
        "compound_id": "Drug-C",
        "metrics": {
          "ic50_nM": 77.68,
          "ec50_nM": 77.68,
          "pIC50": 7.11,
          "ec10_nM": 4.70,
          "ec90_nM": 1284.88,
          "hill_slope": 0.783
        },
        "qc_grade": "green",
        "fit": { "model": "four_pl", "r_squared": 0.9998 }
      }
    ]
  }
}
```

The `flat_line_failure` example returns a red QC grade when response is flat across concentrations. The `few_points_blocking` example returns `has_blocking_errors: true` when fewer than four points are provided per compound.

# Scientific Background

**Dose–response curves.** Inhibition and activation assays relate compound concentration to measured response (e.g. percent viability, luminescence, or normalized signal). Sigmoidal curves are commonly described with logistic models.

**Four-parameter logistic (4PL).** The 4PL model has four parameters: bottom asymptote, top asymptote, IC50 (inflection concentration), and Hill slope. It is widely used for HTS and pharmacology dose–response fitting.

**Five-parameter logistic (5PL).** The 5PL model adds an asymmetry parameter and can fit skewed sigmoidal data. When `model` is `auto`, an F-test selects between 4PL and 5PL.

**IC50 and EC50.** IC50 is the concentration at which response reaches 50% of the fitted range between bottom and top plateaus (absolute mode) or 50% between Top=100 and Bottom=0 (relative mode). EC50 is reported alongside IC50 for the same fitted curve in this tool.

**pIC50.** The negative base-10 logarithm of IC50 in molar units (here derived from nM) is a common potency scale for SAR comparison.

**EC10 and EC90.** Effect concentrations at 10% and 90% of the fitted response range, useful for therapeutic window and steepness reporting.

**Hill slope.** Describes the steepness of the sigmoidal transition around the inflection point.

**Relative vs absolute IC50.** Relative mode fixes Top=100 and Bottom=0, which is common when data are already normalized to percent response. Absolute mode estimates top and bottom from the data; optional `constraints` can fix plateau values.

**Zero concentration.** Points at zero concentration are excluded from fitting.

**Terminology.** Researchers search for dose-response curve fitter, IC50 calculator, EC50 fit, 4PL curve fit, HTS IC50 batch, pIC50 calculator, Hill slope dose-response, and pharmacology curve fitting—these workflows are what the dose-curve-fitter tool addresses.

# Frequently Asked Questions

**What is IC50?**
IC50 is the concentration at which the fitted response reaches 50% of the range between the bottom and top plateaus (absolute mode) or 50% between normalized Top=100 and Bottom=0 (relative mode).

**What is EC50 and how does it differ from IC50?**
EC50 (half-maximal effective concentration) uses the same inflection logic on the fitted curve. This tool reports both `ic50_nM` and `ec50_nM` in the metrics output for each compound.

**What is pIC50?**
pIC50 is −log10(IC50 in molar units). It converts IC50 to a potency scale where larger values indicate higher potency, which is convenient for SAR tables and kinase panel comparisons.

**What is a 4PL dose-response curve?**
A four-parameter logistic (4PL) model fits sigmoidal concentration–response data with bottom, top, IC50, and Hill slope parameters. It is standard for many inhibition and activation assays.

**When should I use 5PL instead of 4PL?**
Use 5PL when the curve is asymmetric. Set `model` to `auto` to let an F-test choose between 4PL and 5PL, or set `five_pl` to force the five-parameter model.

**What is relative vs absolute IC50?**
Relative IC50 assumes Top=100 and Bottom=0 (percent response). Absolute IC50 estimates top and bottom plateaus from your data; you can optionally fix them with `constraints`.

**What regression weighting options are available?**
`none` (unweighted), `1/y`, or `1/y2` weighting can be set via the `weighting` input field.

**How many concentration points do I need per compound?**
Fewer than four points per compound produces blocking errors. The `few_points_blocking` manifest example demonstrates this failure mode.

**What does the QC green/amber/red grade mean?**
Each compound receives a `qc_grade` and plain-English `qc_messages`. Green indicates a good fit within expected ranges; amber and red flag problems such as missing plateaus or flat response (see `flat_line_failure` example).

**What CSV format does the tool accept?**
Optional `csv_text` should include `compound_id`, `concentration`, and `response` columns. Concentrations are handled internally in nM.

**Are zero-concentration points included in the fit?**
No. Zero concentration points are excluded from fitting.

**What metrics appear in the summary table?**
Per compound: IC50, Hill slope, R², pIC50, EC10, EC90, plus QC grade. The web interface also supports bootstrap confidence intervals for IC50 on demand.

**Can I exclude outlier points?**
The web application supports excluding outliers per compound with curve review. Pass excluded points through the web UI workflow; the API returns `points` with an `excluded` flag in full output.

**Does the Python client work offline?**
No. Calculations run on Pepkio servers via the REST API. A network connection and API key are required for `run()`. Manifest fetch works without a key.

**How do I export results for a manuscript?**
The web application supports CSV download of all results, SVG or PDF figure export per compound, and a methods PDF. The API returns structured JSON including `compounds`, `metrics`, and `audit_log`.

**What is Hill slope?**
Hill slope (reported as `hill_slope`) describes how steeply response changes around the IC50 inflection on the fitted logistic curve.

**Can I fit an entire HTS plate at once?**
Yes. Upload or paste a multi-compound CSV, or submit a `compounds` array with one entry per compound ID and its concentration–response `points`.

**How does this compare to fitting one curve at a time in Prism?**
Prism fits individual curves well but is typically used one compound at a time. This tool batch-fits all compounds from one upload and applies consistent QC grading across the panel.

**What happens when response is flat across doses?**
The `flat_line_failure` example yields a red QC badge when response does not change across concentrations, making unreliable IC50 estimates visible before reporting.

# Web Application

For researchers who prefer a graphical interface, an interactive [Dose-Response Curve Fitter](https://www.pepkio.com/tools/dose-curve-fitter) is available in the browser.

The web version provides CSV upload or paste, sample data loading, 4PL/5PL/auto model selection, relative vs absolute IC50 with optional plateau constraints, a summary table of IC50, Hill slope, R², pIC50, EC10, and EC90 with fit-quality flags, per-compound curve review with outlier exclusion, bootstrap CI for IC50 on demand, SVG and PDF figure export, CSV download of all results, methods PDF for manuscripts, shareable links to reopen analyses, and browser storage of recent runs. No account or install is required; screen data stays on your machine.

Use the web tool for interactive review and figure export; use this Python package for scripted analysis, LIMS integration, or batch pipelines.

# Related Resources

GitHub Repository: [https://github.com/pepkio/pepkio-dose-curve-fitter](https://github.com/pepkio/pepkio-dose-curve-fitter)

PyPI Package: [https://pypi.org/project/pepkio-dose-curve-fitter/](https://pypi.org/project/pepkio-dose-curve-fitter/)

Web Application: [https://www.pepkio.com/tools/dose-curve-fitter](https://www.pepkio.com/tools/dose-curve-fitter)

# About Pepkio

[Pepkio](https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and [analysis services](https://www.pepkio.com/cro). Explore additional calculators on the Pepkio website.

# License

MIT

# Keywords

dose-response curve fitter, IC50 calculator, EC50 calculator, pIC50 calculator, 4PL curve fit, 5PL curve fit, four parameter logistic, five parameter logistic, HTS dose-response, high throughput screening IC50, pharmacology curve fitting, Hill slope calculator, EC10 EC90, batch IC50 fitting, multi-compound CSV dose-response, kinase inhibitor IC50, receptor inhibitor panel, SAR pIC50 table, sigmoidal curve fit, logistic regression pharmacology, relative IC50, absolute IC50, dose-response QC, curve fit quality flag, plate reader dose-response, inhibition curve analysis, activation curve analysis, pepkio-dose-curve-fitter, Python IC50 API, REST API dose-response, pharmacology teaching tool, GraphPad Prism alternative IC50, HTS potency analysis, concentration response curve, IC50 from CSV upload, auto 4PL 5PL selection, F-test curve model, regression weighting 1/y, zero concentration exclusion, shareable dose-response analysis, methods PDF dose-response, how to calculate IC50 from dose-response data, how to fit 4PL curve for HTS screen, batch IC50 from plate reader export, compare 4PL vs 5PL dose-response automatically, what is pIC50 for SAR table, relative vs absolute IC50 explained, how many points needed for IC50 fit, flag unreliable IC50 missing plateau, export dose-response curve SVG PDF, Python script IC50 kinase panel, automate HTS IC50 pipeline Pepkio API, dose-response screen CSV format compound_id concentration response, teach pharmacology dose-response without Prism license, reanalyze HTS data with QC grades, EC50 EC10 EC90 from logistic fit, Hill slope interpretation dose-response, flat response red QC dose-response, share dose-response analysis link collaborators, manuscript methods text dose-response fitting
