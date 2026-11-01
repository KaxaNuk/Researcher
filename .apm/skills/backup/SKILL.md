---
name: backup
description: >
  Keep a copy of the researcher's home — or of a strategy — off this computer, on a private GitHub
  repository: make it, send each new saved version there, and bring it back on a new computer.
  Only when the owner asks — "keep a copy", "back up", "save it online", "a new computer", "what
  is a commit", or the same in their language — never offered on its own. It never makes a
  repository public, never forces a send, never pulls or merges on its own, and never creates an
  account or signs in for the owner.
metadata:
  version: 0.3.0
---

# Backup — a copy of your researcher off this computer

Every go saves a version of what it wrote, on this computer only, as the home's `AGENTS.md` says
under *Plan first, then write*. This skill keeps a second copy, on a private GitHub repository,
when the owner asks for one, and only then: no skill reminds them of it, and no hand-over offers
it; the interview's list of uses names it in one line. It is also where a failed send points —
*say* back up *when you want me to look*.

**Plain words.** To the owner a version is never a *commit*, and git is named only when they name
it: *a saved version*, *your copy on GitHub*, *send*. You run every command; show one when asked.

**How to ask.** In Claude Code, the questions below are asked by calling `AskUserQuestion` — the
options as its choices, at most four, and *Other*, which the tool always offers, as the free-text
escape. Without such a tool — Codex and every other assistant — they are one chat message:
each question numbered, its options numbered beneath it, *Other — your own words* last, and one
line on how to answer. Every question, option and line is in the owner's language, and every
header is the one given below for that language — the English one for any other — twelve
characters at most.

## Step 1: What to say first

Two lines, in the owner's language, before a first copy: *Every go saves a version on this
computer only. A copy on GitHub keeps it safe if the computer breaks, and follows you to a new
one — private: only you, and anyone you invite, can see it.* Asked *what is a commit?*: *git's
word for a saved version — a dated snapshot of the files, signed with your name.* A question alone
ends the run there.

## Step 2: Which folder

The researcher's home, by default — the folder that holds `RESEARCHER.md`. When the session is open
in a strategy — `Bibliotheca/`, `Universe/` and `Experiments/` — that strategy: one strategy, one
repository, never inside the home's copy. The worked example, whose `README.md` or `AGENTS.md` holds
the line `<!-- example: begin -->` alone at column 0, as `next` tells it, is for reading and takes
no copy. Name the folder, by path: every git command below but *Step 10*'s clone runs in it, as
`git -C "<it>"` when the session is open elsewhere. A folder with no `.git/` keeps no versions yet:
say so in one line — at home `next` offers to start them — and stop. Changes not saved yet stay out
of the copy: at home `next` offers to save them; in a strategy they are the owner's to save, as its
`AGENTS.md` says.

## Step 3: A copy already?

`git remote get-url origin`. When it prints an address, first make sure the copy is private: with
`gh` signed in, `gh repo view <the address> --json visibility -q .visibility` prints `PRIVATE`;
without `gh`, ask the owner to look on GitHub. A public copy, or one nobody confirms private, is
said in one line — *make it private in its settings on GitHub first* — and nothing is sent to it.
Then say where the copy is and how many saved versions it lacks — after a fetch, as *Step 8* runs
a send, `git rev-list --count "@{u}..HEAD"` — and, when `kaxanuk.autosend` is `paused`, that a
send failed, and why. Saved versions only the copy holds, `"HEAD..@{u}"`, are *Step 8*'s last
paragraph. Then ask `Your copy` (`Tu copia`): *Send the versions not sent yet*, as *Step 8* does;
*Change automatic sending*, *Step 7*'s question; *Nothing now*. When `kaxanuk.autosend` is not
set, *Step 6*'s `E-mail` and *Step 7*'s `Send?` are asked in the same call; when the send
succeeds, `kaxanuk.autosend` goes back to `true` only when it was `paused`. Then stop: the rest is
for a first copy.

## Step 4: Plan and go

In chat, short: the folder; the first way of *Step 5* that applies; the repository's name, and
that it is private; what the copy holds and what stays here (*Step 9*); at home, `settings.yml`'s
change as a diff (*Step 9*); and what is the owner's to do — sign in to GitHub, or create an
account, in any browser window that opens. A home whose `AGENTS.md` has no *Versions* paragraph
gets one line more: `update` brings it, so every skill that saves knows how to send. Then ask, in
one call:

- `Go?` (`¿Adelante?`) — *Go*, *Change something*, *Stop*; in chat, any of the go words in the
  home's `AGENTS.md`. On *Change something*, ask again with options: another name, another way.
  Never act on silence or on a *Stop*.
- `Send?` (`¿Envío?`), as *Step 7* says.

On *Go*: the way; once the copy exists, *Step 6*'s `E-mail`, then the setting *Send?* chose.

**Before the first copy**, and before the plan, run the `security` skill's check on the folder, as
its *Check a folder* says. Something to fix — a key in a file, a file of keys git would save — is
shown, in plain words, and the copy waits until it is fixed and saved: a copy on GitHub keeps every
version it receives. Only things to look at are shown, and the plan goes on.

## Step 5: Three ways, in this order

1. **`gh`, installed and signed in** — `gh auth status` succeeds:
   `gh repo create <name> --private --source "<the folder>" --remote origin --push`, always
   `--private`. `<name>` is `<slug>-researcher` for a home, the researcher's name made safe as
   `interview`'s *Step 4* says — `Sofía` gives `sofia-researcher` — or the strategy's folder name.
2. **github.com** — the owner signs in, or creates a free account: theirs to do. They create an
   **empty private** repository at <https://github.com/new>, by that name, with no README, licence
   or `.gitignore`, and paste its address. Before anything is sent, make sure it is private: with
   `gh` signed in, *Step 3*'s `gh repo view`; without, a probe that uses no stored sign-in, on its
   https address, `https://github.com/<owner>/<name>`, whatever form was pasted:

   ```bash
   GIT_ASKPASS= GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c core.askPass= -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 ls-remote <it>
   ```

   ```powershell
   if (Test-Path Env:GIT_ASKPASS) { Remove-Item Env:GIT_ASKPASS }; $env:GIT_TERMINAL_PROMPT = '0'; git -c credential.helper= -c core.askPass= -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 ls-remote <it>
   ```

   Exit code 0, with nothing printed for an empty repository, is a public one: *Step 3*'s one
   line, and nothing is sent or set. It is private only when the probe fails with git's own
   `could not read Username for 'https://github.com': terminal prompts disabled` — GitHub's answer
   to an anonymous request for a private or missing repository. Any other failure — the network, a
   stall, GitHub busy — is one plain line, *I could not check that your copy on GitHub is private
   (<the reason in plain words>), so nothing was sent*, and nothing is sent or set. Once it is
   private, `git remote add origin <the address>` and `git push -u origin main`, with
   `GIT_TERMINAL_PROMPT=0` set as *Step 8* shows for each shell, so git never waits on a prompt in
   the terminal that no one can answer. The first send may open a browser window asking them to
   sign in to GitHub, once: that is expected, and theirs to do. When it fails with
   `Repository not found` — the address mistyped, or the repository not made yet —
   `git remote remove origin`, say so in one plain line, and ask for the address again.
3. **GitHub Desktop** — when the second fails for want of a sign-in, or they prefer it: *File → Add
   local repository*, the folder, then *Publish repository* with *Keep this code private* ticked.
   `git remote get-url origin` then names the copy.

**Git must be able to sign in to send on its own.** After the first way, `gh auth setup-git`, so
git uses `gh`'s sign-in. After the third, make one send the way the second makes its first —
`GIT_TERMINAL_PROMPT=0` alone, without `credential.interactive=never` — so a browser sign-in can
open once. When git still cannot sign in, automatic sending is not offered: `kaxanuk.autosend`
is `false`, and the copy is updated from GitHub Desktop's *Push origin*, which say in one line.

An owner who wants the assistant to do all of it gets `gh` on their go —
`winget install GitHub.cli` on Windows, `brew install gh` on macOS — and `gh auth login` is their
sign-in, in the browser it opens. Then the first way.

## Step 6: Their e-mail

Every saved version is signed with `git config user.name` and `user.email`, and on GitHub both
travel with it. Since the researcher asks no e-mail, the address is usually empty, `<>`, and a
version shows the name alone. Once they are signed in, ask `E-mail` (`Correo`): *Use GitHub's
private address (recommended)*, which links each version to their GitHub account; and, when
`git config user.email` prints an address, *Keep the one I have*, or, when it prints `<>` or
nothing, *Keep it empty* (*the versions show your name alone*). The private one, ending in
`@users.noreply.github.com`, is on <https://github.com/settings/emails>: ask them to copy it from
there and paste it here. Set for that folder only, `git config user.email <it>`, it signs new
versions only: those already saved keep theirs, and history is never rewritten. At home the choice
also goes in `settings.yml`, as *Step 9* says, so a new computer signs the same way.

If GitHub refuses a send because it would publish a private e-mail — error `GH007` — say so plainly,
and give the two choices: allow it once in GitHub's e-mail settings, or keep the copy as it is.

## Step 7: Sending each new version

Asked once, `Send?` (`¿Envío?`) — *Send each new version automatically (recommended)*, *Only when I
ask*: `git config kaxanuk.autosend true` or `false`, in that folder only, and at home in
`settings.yml` too, as *Step 9* says. With *Only when I ask*, *back up* sends what has piled up, as
*Step 3* does.

## Step 8: Sending a version

What every skill that saves does when `git config --get kaxanuk.autosend` prints `true`, and what
this skill does when asked. It runs with no prompt that nobody can answer, and is given up when
the network stalls for twenty seconds, on an https address or an ssh one. In bash or zsh, on
Windows, macOS or Linux:

```bash
GIT_TERMINAL_PROMPT=0 GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=20' git -c credential.interactive=never -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 push
```

```powershell
$env:GIT_TERMINAL_PROMPT = '0'; $env:GIT_SSH_COMMAND = 'ssh -o BatchMode=yes -o ConnectTimeout=20'; git -c credential.interactive=never -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 push
```

The fetch of *Step 3* runs the same way, `fetch` in place of `push`.

**Before each send**, the `security` skill's script runs on the folder, with no question, as
`uv run --no-project python -I "<the security skill's folder>/scripts/security_check.py" "<the
folder>"`. Exit 2, something to fix, and nothing is sent: the version stays saved here, one plain
line — *Saved on this computer, not sent: <the file> holds what looks like a key. Say* security
*to look at it.* — and `git config kaxanuk.autosend paused`. Exit 0 or 3 goes on; a check that
cannot run (no `uv`) is said in one line, and the send goes on.

Never `--force`; never a pull, a merge or a rebase on its own. On success, one line: *Saved and
sent*. On any failure the version stays saved here; one plain line — *Saved on this computer; your
copy on GitHub could not be updated (<the reason in plain words>). Say* back up *when you want me
to look.* — and `git config kaxanuk.autosend paused`.

When the copy holds versions this computer lacks — saved from another computer — say so, and ask
`Bring?` (`¿Los traigo?`): *Bring them here*, *Not now*. On *Bring them here*, `git pull --ff-only`,
only when nothing here differs: no unsaved change and no saved version the copy lacks; otherwise
stop and explain: two computers saved different versions, and joining them is the owner's choice.

## Step 9: What the copy holds

What the folder's saved versions hold, and nothing its `.gitignore` keeps out. At home: the notes,
the studies, the lessons, `Philosophy/`, `RESEARCHER.md`, `settings.yml` and the clippings in text;
**not** the
PDFs and other files kept out of `Sources/`, nor `Extracts/`, `Briefs/`, `Portfolio/` or any
`.env` — they stay on this computer by design. In a strategy: the code, the documents and the
notes; not the PDFs, the data, the engines' output or `Config/.env`. Suggest keeping the PDFs and
`Portfolio/` somewhere private of their own — a personal cloud folder outside the home, or an
external disk — never in this copy, and never force a kept-out file into it.

**At home, `settings.yml` travels in the copy**, so a new computer is set up from it. On *Step 4*'s
go, and on *Step 3*'s *Send* when the file lags, `backup` writes two parts of it, shown in the plan
as a diff and nothing else touched: `versions:` — `email` as *Step 6* chose, `"<>"` for none, and
`send` as *Step 7* chose — and `assistants:`, adding each one `~/.apm/apm.yml` lists under
`targets:` that the home's `apm.yml` lists too, read with the file tool. Then it saves that file
alone, `git add settings.yml` and `git commit -m "Backup: settings"`, and a send carries it: on
*Step 3*'s *Send*, the one it makes; on a first copy, whose first send comes before *Step 6*'s
e-mail and *Step 7*'s setting, one more send as *Step 8* does, whatever *Send?* chose — the owner
asked for this copy, and it holds their choices only once that version is in it. A home
without the file gets it first from the template, by the script in the `init-strategy` skill's
folder, run from the home's root, never written from memory —
`scaffold.py researcher . --only settings.yml`, as `update` runs it. A strategy has no
`settings.yml`.

## Step 10: A new computer

Install the package as the package's `SETUP.md` says — git and uv in its step 1, the package in its
step 2; the README's line for bringing a researcher back runs both and this step. Then clone the
copy into a short folder — `git clone <the address> <folder>`, the address the owner pastes, or,
with `gh` signed in, the one they pick from `gh repo list --visibility private` — and run `update`
there, in the same session. `update` rewrites the researcher's skill and the agent's path for the
new folder, installs the home for the user and sets this computer up from `settings.yml`: the
package and the home for each assistant it lists, the e-mail and `kaxanuk.autosend` from its
`versions:`, and the brief, through `brief setup`, which asks only for the go. A choice the file
leaves empty — or a home from before it — is asked again: the e-mail and *Send?* as *Step 6* and
*Step 7* say; the name at the first save, as any save asks it. A strategy's clone takes its own
`SETUP.md` instead. The PDFs and `Portfolio/` come from wherever they were kept, and `Extracts/` is
made again by `read`'s script. Then a new session, where the researcher is.

## Never

A public repository, or making one public; `--force`, or rewriting history; creating an account or
signing in for the owner; storing a token or a password — in a file, an address or a setting; a
pull, a merge or a rebase on its own; sending anything when `kaxanuk.autosend` is not `true` and
the owner did not ask; offering a copy, or reminding the owner of one, unasked.

## References

- The home's `AGENTS.md`, *Versions*: what a saved version is, and the send each saving skill makes.
- `next`: at home, starts the versions where there are none, and saves changes made by hand.
- `update`: on a new computer, rewrites the researcher's skill and the agent's path for the new
  folder, installs the home, and sets the computer up from `settings.yml`.
