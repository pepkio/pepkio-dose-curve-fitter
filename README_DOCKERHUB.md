# Pepkio Dose-Response Curve Fitter

Run the Pepkio dose-curve-fitter CLI in a container to batch-fit HTS dose–response curves and obtain IC50, pIC50, and QC grades through the hosted API.

# What It Does

The image runs `pepkio-dose-curve-fitter`, a client for the Pepkio Dose-Response Curve Fitter REST API. Submit multi-compound concentration–response data (CSV or structured JSON); receive 4PL/5PL fit parameters, per-compound IC50, EC50, pIC50, EC10, EC90, Hill slope, R², and green/amber/red QC grades with plain-English messages.

Typical workflows include HTS IC50 panels, kinase inhibitor SAR tables, pharmacology teaching, and QC review before reporting. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Models: `four_pl`, `five_pl`, or `auto` (F-test)
- IC50 modes: relative or absolute with optional constraints
- Weighting: `none`, `1/y`, or `1/y2`
- Per-compound metrics and QC grades
- Named manifest examples (`hts_batch_absolute`, `relative_ic50`, etc.)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/dose-curve-fitter:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/dose-curve-fitter:0.1.0 \
  pepkio-dose-curve-fitter run --example hts_batch_absolute
```

Manifest only (no API key):

```bash
docker run --rm pepkio/dose-curve-fitter:0.1.0 \
  pepkio-dose-curve-fitter manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/dose-curve-fitter:0.1.0 \
  pepkio-dose-curve-fitter run --example relative_ic50
```

# Typical Use Cases

- Batch IC50 fitting from a multi-compound HTS CSV in CI pipelines
- Kinase panel potency extraction with pIC50 for SAR tables
- Fixed-environment workflow runners for pharmacology analysis
- QC screening for flat responses or insufficient dose points
- Automated reanalysis of dose-response exports in pipelines

# Scientific Background

4PL and 5PL logistic models fit sigmoidal concentration–response data. IC50 is the inflection concentration; pIC50 is −log10(IC50). Relative mode fixes Top=100 and Bottom=0; absolute mode estimates plateaus. Zero concentration points are excluded. Fewer than four points per compound returns blocking errors.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/dose-curve-fitter

The web UI adds per-compound curve review, outlier exclusion, bootstrap CI for IC50, SVG/PDF export, methods PDF, shareable links, and reload of recent runs.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-dose-curve-fitter

Web Application: https://www.pepkio.com/tools/dose-curve-fitter

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.
