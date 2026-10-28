---
name: init-strategy
description: >
  Create a new KaxaNuk strategy repository in a new folder, from the KaxaNuk Strategy Template that
  ships inside the researcher package — copied by a script, byte for byte, its first version
  saved. Only when the owner runs it by name; the strategy's name is always theirs — with none
  given, it asks what the idea is and suggests names to pick. It does NOT set up the
  environment or the keys (the new folder's SETUP.md does), does NOT copy the worked example (use
  `init-example`), does NOT create a researcher (use `init-researcher`), and does NOT create a
  Python library (use `init-python-library`).
metadata:
  version: 0.4.4
---

# Init strategy — a new strategy, one folder, one repository

The owner starts a new strategy. What they said carries the arguments: the strategy's name, always
theirs, which becomes the folder and the repository — `fcf-yield-quality`, not `Experiment` — where
to put it, and optionally one sentence on the idea. One strategy is one repository: never create a
strategy inside another strategy, inside the researcher's home, or inside this package.

**The copy is the script's, never yours.** A file of the template is never written from memory, so
every strategy made from the same package version starts identical.

## When to Use

- The owner runs `init-strategy` by name — *init-strategy fcf-yield-quality*, *start a new strategy
  called …*.
- Not on its own initiative, and not to repair an existing strategy. A file of the template that
  the strategy lacks — lost, or never there because the strategy was made before template 0.10.0
  shipped the drivers, notebooks and documents — comes back from the template, never from the
  example, whose copy is filled in. Run this skill's script from the strategy's root; it never
  overwrites a file.

  ```bash
  uv run --no-project python "<this skill's directory>/scripts/scaffold.py" strategy . --only <path>
  ```

## Steps

1. **What it is about, then its name — always the owner's — and the place.** The name becomes the
   folder and the repository, and at the new folder's `SETUP.md` step 5 the name in
   `pyproject.toml`: lowercase ASCII letters with no accents, digits and single hyphens. Any name of
   theirs — with the command, `init-strategy fcf-yield-quality`, in their words or under *Other* —
   is put in that form, *Momentum México* giving `momentum-mexico`, and shown in the plan. One with
   nothing left in that form is said in one line, and another of theirs asked for; with one, go on
   to the place. Without one, when what they said does not yet tell what the strategy is about,
   first ask in one short chat message — *Tell me the idea in a sentence or two — what it would buy,
   and why you think it works — and I'll suggest a few names* (*Cuéntame la idea en una o dos frases
   — qué compraría y por qué crees que funciona — y te sugiero unos nombres*) — with nothing else
   asked or run before the answer. Words after the command that are not one name are the idea; a
   name in the answer is theirs. From their words on the idea, offer two or three names through the
   question tool, header `Name` (`Nombre`), each short and made from what they said — *momentum in
   Mexican stocks* gives `mexico-momentum` — and described by the folder it makes, none whose folder
   is already there. *Other* takes a name of their own. With no question tool, the names are a
   numbered list in chat, *or type your own*. Never a name they did not pick or type, and never a
   placeholder such as `my-strategy` or a literal `<name>`. Their words on the idea, any name aside,
   are what step 4 repeats.

   The place: the parent of the folder the session is open in, so a strategy lands beside the
   others, `D:\Research\fcf-yield-quality`, unless they say another. A folder of that name already
   there and not empty is said in one line, and another name or place asked for — theirs, typed or
   picked from names offered as above, their idea asked first if not yet said; never a suffix such
   as `-2`. On Windows, keep it short: a deep synced path such as `C:\Users\<you>\OneDrive\...`
   breaks tools later with misleading errors such as `WinError 3`. Say the full path you will
   create.

2. **The plan.** In chat: the path, that it will hold the KaxaNuk Strategy Template at this
   package's version, and that it keeps dated versions from the start, the first saved now. Say too
   that nothing else on the machine changes, the date of the weekly version check in the home's git
   config aside. When a newer package is out, checked and dated as item 5 of *Step 4* in the `next`
   skill beside this one says — never with `updatereminder` off or an `updatenext` still ahead — one
   more line: *a newer version of the package is out, X.Y.Z: `update` first brings the newest
   template*. Never a question of its own, and the copy never waits on it. Ask for the go — *Go*,
   *Change something*, *Stop* — and run on *Go* only.

3. **Copy.** The script is in this skill's folder:

   ```bash
   uv run --no-project python "<this skill's directory>/scripts/scaffold.py" strategy "<full path>"
   ```

   It takes a leading `~` as the home folder, and refuses a folder that exists and is not empty,
   saying why; then ask, as step 1 does, for another name or place, rather than going around it. On
   Windows without long paths, it also refuses a destination so deep that a copied path would pass
   259 characters, names that path and the longest destination that fits, and writes nothing; ask
   for a shorter place. A copy the system stops partway — a full disk, a file refused — ends in one
   line naming the file and the reason; the partial folder can be deleted. If it cannot find the
   package, it prints the install command — give it to the owner. A fork of the package, or a clone
   in a folder of another name, is not found on its own: pass `--package <its install folder>`. A
   git step that fails leaves the copy in place — the script still exits 0 — and prints every
   command that finishes the repository from that step on. If git is missing, install it on the
   owner's go, then run the printed commands in the new folder. If the first commit fails for want
   of a git identity, ask in one open message, with no options, *What's your name, or what would
   you like me to call you?*, never invented, and no email; set them in that folder only,
   `git config user.name "<their answer>"` and `git config user.email "<>"`, an empty address,
   then run the printed commands there.

4. **Hand over.** Tell the owner to open the new folder in a **new** session and follow its
   `SETUP.md` from step 2. Repeat their words on the idea, if any, for them to give the new session
   at its `SETUP.md` step 5, the README's first line; then `OBJECTIVE.md`, before any paper.

## References

- `scripts/scaffold.py`, in this skill's folder — copies `templates/strategy/` from the
  KaxaNuk Researcher package; `--help` has every option. `init-researcher`, `init-example` and
  `init-python-library` run the same script, and `init-example` lists the examples with it,
  `scaffold.py examples`, every folder `examples/<kind>/<name>/` of the package.
