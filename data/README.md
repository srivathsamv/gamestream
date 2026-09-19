# data/

This folder holds cached historical data pulled by
`gamestream/ingestion/statsbomb_loader.py`. It's gitignored except for this
file — regenerate it locally by running the ingestion script rather than
committing raw data to the repo.

Suggested layout once populated:

```
data/
  raw/          untouched events pulled from StatsBomb open data
  processed/    cleaned/aggregated data (e.g. the Stage 1 lookup table)
```

## Licensing

StatsBomb's open data is released under **CC BY-NC-SA 4.0** via their
[public data user agreement](https://github.com/statsbomb/open-data):
attribution required, non-commercial use only, share-alike. This project
is a personal/portfolio project, which fits — just don't repurpose this
data or derived models commercially without checking the license again.
