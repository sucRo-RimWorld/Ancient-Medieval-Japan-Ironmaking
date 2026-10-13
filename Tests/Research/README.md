# Temporary research tests

Opt-in only; no active experiments. Never include in default CI or normal test discovery. Record question, owner, evidence destination and retirement condition before adding an experiment.

The historical MO startup differential check is opt-in only:
`python -m unittest discover -s Tests/Research -p 'test_mo_startup_matrix.py' -v`.
It checks the *diagnostic harness* and does not establish loaded MO or Ironmaking.
The routine source/runner CI intentionally excludes this retired startup investigation.
