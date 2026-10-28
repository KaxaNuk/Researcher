"""
Time series -- step 3 of 8: how every per-security file is stored, and the one way it is read.

In plain words: every price file, curated or refined, is a Parquet file read and written with
PyArrow, so a step reads only the columns it asks for and never parses text.

Runs inside every stage that touches a per-security file: `Data/curator.py`, `Data/refinery.py`,
the universe and analyzer notebooks, and the experiments' seams.  Each imports it from `Data/`, a
folder rather than a package, so each puts `Data/` on the import path first.

What is expected here:

- One schema for every file: the date as `date32`, every other numeric column as `float64`, and a
  text column -- an identifier, a `current_*` classification -- kept as text.  The Data Curator can
  write a provider's prices as decimals whose precision changes from file to file, and its volume
  as integers; read as they come, two files would not stack, and the engine and pandas would each
  read them their own way.  So every file the Curator writes is rewritten in the shared schema
  before anything reads it.  A decimal cast to `float64` is the same number a CSV of it parsed to.
- One place that names a file: the identifier and the suffix, `<identifier>.parquet`, in the
  folder of the stage that wrote it.
- Read only the columns asked for, from the file's footer first.  A file of eighteen columns read
  for two is the difference between a step that loads a quarter of a century in seconds and one
  that loads it in minutes.  A caller stacking many files stacks them as Arrow tables and converts
  to pandas once.
- Name a missing column in the error, before anything is read.

It produces nothing of its own: it is how `Data/Curator/Time_Series/` and
`Data/Refinery/Time_Series/` are written and read.

It prevents two stages reading the same file two ways, and a run that spends its hours parsing
text instead of computing.
"""
