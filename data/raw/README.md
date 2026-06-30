# Raw PLFS Data — Not Redistributed

This folder is where your PLFS microdata extract should be placed before running
`src/plfs_real_analysis.py` (expected filename: `plfs_large.csv`, or update
`DATA_PATH` in the script).

**The actual PLFS microdata file is intentionally not included in this repository.**

PLFS unit-level microdata is released by MoSPI subject to its own terms of use.
Redistributing the raw file via a public GitHub repository is not appropriate.
This is standard practice for projects built on government or licensed microdata:
share the code and the methodology, not the restricted raw file.

## How to get the data yourself

1. Go to [mospi.gov.in/web/plfs](https://mospi.gov.in/web/plfs)
2. Register for free access to unit-level microdata
3. Download the PLFS annual round of your choice
4. Place the extracted CSV in this folder
5. Update `DATA_PATH` at the top of `src/plfs_real_analysis.py` if your filename differs
6. Run `python src/plfs_real_analysis.py`

See `data_dictionary_PLFS_real.md` in the project root for the exact column
names and structure the analysis script expects.
