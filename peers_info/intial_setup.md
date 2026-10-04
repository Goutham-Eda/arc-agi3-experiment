Step 1. Publish your current agent on Kaggle as a public notebook

Why: Right now you can't legally share any code with your peers. Publishing one piece of code publicly fixes that, because public code is allowed to be seen by everyone. It also enters you for the Milestone 2 prize.

How:
1. Take submission/my_agent.py (the random + pruning agent).
2. Make it a Kaggle notebook on the ARC-AGI-3 competition page.
3. Set the licence to Apache-2.0.
4. Click Publish so it is public, not private.
5. Copy the notebook link and save it.

Deadline: September 30. That's 6 days away.

What you're giving up: almost nothing. That agent scores 0.07. Your real work — the E1–E4 harness and the P1–P8 designs — stays private.

Done when: you can open the notebook link in a private browser window and it loads.

---

Step 2. Put the experiment skill in a public GitHub repo

Why: This is the thing your peers actually follow. It has no competition code in it, so anyone can have it.

How:
1. The files are ready at …/scratchpad/arc-agi3-experiment/. Read them first.
2. Make a new public GitHub repo called arc-agi3-experiment.
3. Copy the nine files in.
4. Add an Apache-2.0 licence file.
5. Push.

Done when: a stranger can clone it and read SKILL.md.

---

Step 3. Decide who is doing what

Why: Five people all "helping" with no owners means nothing gets finished.

Open your design doc's portfolio table and assign one experiment per person:

┌────────────┬───────────────────────────────────────────────────────────┬──────────────────────────────────┐
│ Experiment │               What it asks, in plain words                │             Hardware             │
├────────────┼───────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ P1         │ Do we misjudge when the screen changed, because clocks    │ Laptop                           │
│            │ tick?                                                     │                                  │
├────────────┼───────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ P2         │ Should we click on objects instead of random spots?       │ Laptop                           │
├────────────┼───────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ P3         │ Can it learn during a game which buttons do something?    │ Laptop                           │
├────────────┼───────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ P4         │ Does remembering where it's been, and going back, help?   │ Laptop                           │
├────────────┼───────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ P5         │ If it already knew the goal, how much better would it do? │ No computer needed — pen and     │
│            │                                                           │ paper                            │
└────────────┴───────────────────────────────────────────────────────────┴──────────────────────────────────┘

Give P1 to your most reliable person. The other four depend on it.

Done when: each name has exactly one experiment next to it.

---

Part 2 — How a peer joins (copy this part and send it to them)

Step 4. They sign up for Kaggle and accept the rules

They go to the ARC-AGI-3 competition page, register, and click accept.

Important: doing this makes them an official competitor, even though they only want to write the paper. That means you cannot send them your private code, ever. That's fine — they don't need it.

---

Step 5. They download the games themselves

You cannot send them the games. It's against the rules. They download the competition data from the competition page and unzip it.

They will end up with a folder called environment_files.

---

Step 6. They install the software

python -m venv .venv
source .venv/bin/activate          (Windows: .venv\Scripts\Activate.ps1)
pip install arc-agi arcengine numpy pytest

No GPU. No API key. No paid account. A normal laptop is enough.

---

Step 7. They tell the code where the games are

export ARC_ENV_DIR=/path/to/environment_files       (bash)
$env:ARC_ENV_DIR = "C:\path\to\environment_files"   (PowerShell)

They never edit a line of code to do this.

---

Step 8. They pass the day-one test

Why: If their setup is broken, everything they produce later is garbage. Better to find out in hour one.

They run your public notebook's agent on the public games and check four things:

1. It finds the games.
2. Every game starts at level 1. If any starts higher, their setup is reusing the game world between tries. Stop and fix.
3. No level gets cleared in fewer than 5 moves. A 1-move clear is always a bug.
4. The score is near zero and very few levels get cleared. That's correct — random play is bad. If they see a great score, something is wrong, not right.

Done when: all four check out. Only then do they get an experiment.

---

Part 3 — How one experiment runs (every peer repeats this)

This is the loop. It takes about a week per experiment.

Step 9. Write down the plan before running anything

They fill in templates/prereg.md. Twelve questions. The two that matter most:

- "What number counts as success?" — decided now, not later.
- "What result makes me give up?" — decided now, not later.

Why this matters: if you decide what success looks like after seeing the numbers, you will always find something that looks like success. Writing it first is the whole method.

They send it to you. You read it and approve it. You are reviewing their thinking, not their code — that keeps you inside the rules.

---

Step 10. Smoke run

Run it on one game. Does the program finish without crashing? That's all you're asking. No conclusions.

---

Step 11. Probe run

Run it on the practice games with just a couple of settings.

The question here is not "did it work?" It's "is my program actually doing what I said it does?" Is the new feature actually switched on? Is the comparison version actually different?

Why this step exists: without it, when you get a bad result you won't know whether your idea was wrong or your code was broken. Those need completely different responses.

---

Step 12. Practice run (the "tune" games)

Run properly on the 8 practice games.

Two things can happen:
- It looks hopeless → their give-up rule from Step 9 fires. Stop here. This is a finished experiment. Write it up. Three of your five experiments ended exactly this way.
- It looks promising → they lock in the settings and move on. They do not report this as a result. Practice games can kill an idea but can never prove one.

---

Step 13. Real run (the 17 held-out games)

This is the verdict. Run it once, exactly as written in Step 9.

They do not peek at these games earlier. Not once, not "just to check."

---

Step 14. Write up the result

They fill in templates/result.md. The parts people skip and shouldn't:

- The safety checklist — fresh game each try, every game started at level 1, no impossible fast clears, and the run can be replayed to get the same answer.
- The per-game table. Not just the total. Ask directly: is this whole result coming from one lucky game? This has already happened to you once — a doubled score that was almost entirely one level of one game.
- "Did my idea fail, or did my code fail?" Answered out loud, using the probe run as evidence.

A negative result is a real result. Write it up exactly as carefully as a positive one.

---

Step 15. Never edit an old result

If they later find a mistake, they add a new dated note underneath saying what changed and why. The original stays visible, even though it's wrong.

Why: a research record where nothing was ever wrong is a record nobody was checking. Your replay-bug correction is one of the most credible things in your whole project.

---

Part 4 — The weekly rhythm

Once a week, everyone posts two things:

1. Before running: their one-page plan (Step 9).
2. After running: their one-page result (Step 14).

You review the plans. You do not review their code — you don't need to, and staying out of their code keeps the rules clean.

Keep everything in a shared repo or Discord channel. Nothing important lives in a chat message.

---

Part 5 — The paper at the end

The paper is not "we tried to win ARC-AGI-3." It's the bigger question:

▎ How do you drop an agent into a world it has never seen, and know whether each thing you added was actually needed?

ARC-AGI-3 is just the example you used.

Its shape:
- The problem: you added five capabilities to an agent. None beat random play. That's the motivation.
- The evidence: your peers' P1–P5 experiments — the simple, cheap controls that show which capabilities are genuinely necessary.
- The method: decide the falsifier first, separate practice games from verdict games, report every game individually, correct errors in public.

Each peer is a co-author on the experiment they personally planned and ran. That's real credit, and it's why this is worth their time rather than a favour to you.

---

The calendar

┌────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│  By when   │                                             What                                             │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Sept 30    │ Public notebook live (Milestone 2 deadline)                                                  │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Sept 30    │ Skill repo public; peers invited                                                             │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Early Oct  │ Everyone passes the day-one test; plans written and approved                                 │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Through    │ P1 first, then P2–P5 run in parallel                                                         │
│ Oct        │                                                                                              │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Oct 26     │ Team merger deadline — anyone joining your competition team must be merged by now.           │
│            │ Paper-track people are unaffected.                                                           │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Nov 2      │ Final competition submission                                                                 │
├────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ After Nov  │ Write the paper together                                                                     │
│ 2          │                                                                                              │
└────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

---

Two things to keep straight, and everything else follows:

1. Nothing private ever leaves your repo. Only the public notebook and public writing go out.
2. Nobody runs anything until they've written down what would prove them wrong.

If you want, I can turn this into a shareable web page for the group, or draft the actual invite message you send them.s
