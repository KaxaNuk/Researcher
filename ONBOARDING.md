# The onboarding, as approved

> **Frozen.** This is the run the package's owner walked through and approved on 2026-10-10, on
> package 1.10.2, from a clean home on Claude Code, in English: every question and message a new
> user sees, from the language to the end of the first read. `FROZEN.json` fingerprints the files
> that produce it, and `AGENTS.md` says how a frozen file may change. A change to any of them is a
> change to this run: show it against this file first. The line on what the researcher is, under
> *2. The name*, joined the run on the owner's word at 1.11.2; at 1.15.1, on the owner's word,
> question 1 became one open chat message with no options and no number, its question alone,
> asking for the projects and topics too; at 1.15.2, on the owner's word, the name is asked as one
> open question, *or what you'd like me to call you*, and no e-mail is ever asked — `read`'s own
> save included, at 1.15.3. At 1.17.0, on the owner's word, `read` offers a scan a searchable copy,
> reads a page's image for what an extract dropped, and lists its sources and updates existing
> concept pages by script; this run is unchanged, its paper having a text layer and its concept
> pages being new. At 1.19.0, on the owner's word, `SETUP.md` gains a way back for a researcher
> kept on GitHub — a second line to paste, step 3's first paragraph, *Later*'s *A new machine* —
> which a newcomer's run never reaches: this run is unchanged.

What varies from run to run: the language — in Spanish every line is in Spanish, with the headers
the skills give — the names proposed, the paths, the owner's answers and what is proposed from
them, and the document read. So do the words the skills leave to the run: the header `Name`, the
`Where?` question's text, `read`'s `Go?` header and its *Write this plan?*, and the reply to *I
have a document*. Branches off this run's path are as the frozen skills give them. Here git knew
the owner only by the handle `tester`.

How it began: the package had just been installed for the test user, as `SETUP.md`'s step 2 does,
and the run was `init-researcher` from its first step, the language; so `Where?`'s *Go* says
nothing about bringing the package up to date. From the README's pasted line, `SETUP.md` runs
first — git, uv and the install, a progress line each — and opens the name question with *The
package is installed; now your researcher.* When git has no name at all, `SETUP.md`'s step 1 asks
for it before the install, in one open chat message with no options — *What's your name, or what
would you like me to call you?* — and asks no e-mail: versions are signed with the name alone.

## 1. The language

Question `Idioma/Lang`: *¿En qué idioma prefieres que hablemos? / Which language would you like to
use?* — *Español*, *English*, and *Other*. Answered: *English*.

## 2. The name

> Your researcher will be your companion for your work and your projects, and you'll call it by
> its name in any folder. It's for research and learning, never investment advice: it can be
> wrong, every decision is yours, and what you share with it goes to the company behind your
> assistant.

Question `Name`: *What would you like to call it?* — *Nova* (*Bright and quick: new ideas, plainly
put*), *Atlas* (*Steady: carries your whole library for you*), *Iris* (*Clear-eyed: notices the
detail that matters*), and *Other*. Answered, typed: *Arya*.

## 3. Where

Question `Where?`: *Where should I make Arya's home?* — *Go — make it at `<path>`* (*Creates your
researcher's home there, then two quick questions about you, and sets it up — about three
minutes*), *Another folder*, *Stop*. Answered: *Go*.

## 4. The copy, and question 1 in the same turn

> Your assistant may ask you to allow a few commands; allowing them is all you need to do.

The home is copied and the interview's checks run, with no report and no stop. Then:

> Your researcher's home is ready at `<path>`. Now two quick questions about you, so it is yours.
>
> I'm Arya, and I'll speak English; tell me if that's wrong.

Question 1, in the same message, with no box, no options and no number: *First, your name, or what
you'd like me to call you — I only have `tester`. Then tell me more about yourself: what you do,
and the kinds of projects and topics we'll be working on together.* Answered, typed in chat:
*Arturo, and im working in investment research*.

When git has the owner's full name, the question starts at *Tell me more about yourself*, and the
line before it reads *I'm Arya, I'll work for <owner>, in English; tell me if any of that is
wrong*.

## 5. Question 2

Question `Voice`: *2 of 2 · How should I talk to you?* — *Explain as you go* (*Plain words, every
new term explained — for someone new to this*), *Thorough, push back on evidence* (*Full answers,
and a challenge where the evidence disagrees*), *Brief, push back on evidence* (*Short answers, and
the same challenge*), *Thorough, argue the other side* (*Full answers, and the strongest case
against your view*). Answered: *Brief, push back on evidence*.

## 6. Written, set up and saved, with no question

> I'm setting myself up on this computer; your assistant may ask you to allow a few commands.

`RESEARCHER.md`, the agent, the researcher's skill, `apm.yml`, `LICENSE` and the README's opening
paragraph are written from the two answers, installed for the user and saved. From the answers:
*Works for: Arturo, working in investment research*; the voice. Proposed: *Here for: Organise what
I read, and help with my projects*; *Domains: Finance, Macro*; the README's opening paragraph.

## 7. The hand-over

> Saved.
>
> I'm Arya, and from now on I'm in every folder: open a **new** conversation in my home and say my
> name.
>
> My home is `<path>`. I wrote who you are and how I speak, and proposed — what you're here for:
> help with your work and your projects; your domains: Finance, Macro; the opening of your README —
> tell me to change any of it, any time.

Question `First step`: *My first recommendation: give me something to read — I learn from what you
give me. Put the books, papers, articles and notes you want me to read in your Sources folder —
`<path>\Sources`, in Books, Papers or Clippings — or attach one here, and we read it together now.
Shall we start with one?* — *I have a document (recommended)* (*A book, a paper, an article or
your notes: attach them here, or say where they're saved; I copy them into `Sources` and read them
with you, one at a time*), *Suggest a reading* (*A few papers on what you came for, found by their
titles*), *Later* (*Put files in `Sources` any time, or attach them, and say `read`*). Answered: *I
have a document*.

> Attach it here, or tell me where it's saved — several are welcome: I copy them into `Sources` and
> we read them one at a time.

## 8. The first read

The owner attached *Prospect Theory.pdf*. The paper's outline was extracted where it lay, and the
home had no reading question yet, so it was asked first.

Question `Reading for`: *What do you want this reading to help you answer?* — *How do people really
decide under risk?* (*The paper's own question*), *How do gains and losses shape investors?*,
*Which biases should my research account for?* (*From your work in investment research*),
*Background reading, no question in mind*, and *Other*. Answered: *How do people really decide
under risk?*

The paper — one line: read whole, for question 1 — was not asked about again: `read` asks nothing
more of a source whose question was given earlier in the session. The whole extract was read, and
the plan shown in chat: the copy into `Sources/Papers/`; question 1 added to `RESEARCHER.md` in the
owner's words; the note
`Knowledge/Finance/Kahneman_Tversky_1979_Prospect_Theory.md`, its headings the paper's eight claims
with their pages; six concept pages — prospect theory, loss aversion, reference point, certainty
effect, decision weights, isolation effect; the index and the log; tags by the loose policy; no DOI
printed, so `source` says so.

Question `Go?`: *Write this plan?* — *Go* (*Write it and save a version*), *Change something*,
*Stop*. Answered: *Go*.

> Saved.

Then the report: what was written; the gap — the reading map pairs the paper against Fama (1970), a
lead for `Sources/Papers/`; the investing questions of the owner's philosophy it bears on — here Q4,
Q6, Q8, S1 and S2, from the *Bears on* table of `philosophy`'s `references/questions.md`, which is
not frozen — with round 1 of `philosophy investing` offered in a new conversation. `read` puts
*Saved* after the report; in this run it came first. And the hand-over's end, now that the first
document is read:

> **What else you can ask me** — on Claude, type them with a slash, `/read`:
>
> - `read` a PDF or an article, then ask me about it: answers from what you've read, cited
> - `study <a goal, a plan or a decision>`: worked out from your library
> - any project, work or personal: open your assistant there and say my name
> - remember this: a rule or a way of working, kept in my home
> - `brief setup`: a brief on the days you choose — your work, the markets, your holdings
> - `teach <a topic>`: a lesson a session, with a quiz
> - learn to invest from scratch: `philosophy investing`, in a new conversation — one idea after
>   each answer, no reading needed
> - `philosophy`: how you work, or how you invest, in your words, and the rules I keep with you
> - `init-example`, then `init-strategy <name>`: an investment strategy, tested with the KaxaNuk
>   Investment Lab
> - `init-python-library <name>`: a Python library of your own
> - keep a copy: your home on a private GitHub repository
>
> More on each, step by step: <https://github.com/KaxaNuk/Researcher/blob/main/USE-CASES.md>
>
> **Next:** ask me about it — *what does prospect theory say about why people hold on to losers?*
>
> Not sure what's next? Say `next`.
