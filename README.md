# Validation of Linear Ion Accelerator

This repository contains benchmark studies to validate linear ion accelerator beam transport simulations by comparing results across multiple accelerator codes.

## Quick overview

- Focus: compare beam dynamics outputs (phase space, envelopes, losses, and transport metrics) for a LEBT-style line.
- Inputs and reference datasets are stored under `inputs/`.
- Code-specific studies and outputs are organized in:
  - `rftrack/`
  - `Tracewin/`
  - `opal/`
  - `travel/`
- Comparative plots and final figures are available in folders such as `resultados_finales/`, `space_charge/`, and `elipses finales/`.

## Libraries / tools used

- **RF-Track** (`rftrack`): beam dynamics tracking and analysis workflows.
- **TraceWin** (`Tracewin`): reference accelerator simulation outputs and comparisons.
- **OPAL** (`opal`): particle tracking and loss analysis data.
- **TRAVEL** (`travel`): transport simulations and associated post-processing.