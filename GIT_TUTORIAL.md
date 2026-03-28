# Git Tutorial: Version Control for Neuroscientists

**Project:** Leaky Integrate-and-Fire Neuron Simulator  
**Approach:** You downloaded this as a ZIP — no git history yet. You'll build it yourself.

---

## How this tutorial works

You have the project files but no git history — just like starting a project from scratch. 
By the end you'll have:

- A complete local git history with meaningful commits
- The project backed up on GitHub
- Experience with branches, merges, and pull requests
- An understanding of what cloning is and when to use it instead of a ZIP

**The files you already have:**

```
lif-neuron/
├── README.md       ← project description
├── neuron.py       ← LIF neuron class
├── simulate.py     ← runs simulations
└── plot.py         ← plots results
```

Run the code first so you know what it does:

```bash
pip install numpy matplotlib
python simulate.py
python plot.py
```

Now let's put it under version control.

---

## Part 1 — Your First Commits

### Step 1.1 — Tell git who you are (first-time setup only)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "nano"   # or vim, code, etc.
```

These get attached to every commit you make, on any repo.

---

### Step 1.2 — Initialize a git repository

Inside the `lif-neuron` folder:

```bash
git init
```

Git creates a hidden `.git/` folder. That folder *is* your version history — don't delete it.

```bash
ls -a    # you'll see the .git folder
git status   # shows all files as "untracked" — git sees them but isn't tracking them yet
```

---

### Step 1.3 — Add a .gitignore before anything else

Some files should never be committed: large data files, plots, compiled bytecode. 
Tell git to ignore them *first*, before you commit anything else.

Create a file called `.gitignore` with this content:

```
*.npz
*.png
__pycache__/
*.pyc
.DS_Store
```

Now commit just the `.gitignore`:

```bash
git add .gitignore
git status          # .gitignore is staged; the .py files are still untracked
git commit -m "Add .gitignore"
```

> **Why first?** If you accidentally commit a large file, removing it from history is painful.  
> Committing `.gitignore` first makes it impossible to accidentally stage ignored files.

---

### Step 1.4 — Commit the project files

Now stage and commit the actual code. Do it in two commits — one for the model, one for the scripts — to practice making commits that each represent one logical change:

```bash
git add neuron.py
git commit -m "Add LIF neuron class"
```

```bash
git add simulate.py plot.py
git commit -m "Add simulation and plotting scripts"
```

Check your history:

```bash
git log --oneline
```

```
c3d9e1f Add simulation and plotting scripts
b7a2d44 Add LIF neuron class
e9b0a11 Add .gitignore
```

> **Commit messages:** Write them like "Add X", "Fix Y", "Update Z" — short, active, specific.  
> `"misc changes"` or `"asdfgh"` will haunt you in six months.

---

### Step 1.5 — Make a change and commit it

Edit `neuron.py`: change the spike threshold from `-50.0` to `-48.0` mV (a more excitable neuron).

```bash
git diff neuron.py      # see exactly what changed before staging
git add neuron.py
git commit -m "Lower spike threshold to -48 mV"
```

Run `git log --oneline` again. Your history is growing.

---

### ✋ Checkpoint 1

```bash
git log --oneline
```

You should have 4 commits. If something looks wrong, `git status` will almost always tell you what to do next.

---

## Part 2 — GitHub: Backing Up and Sharing

A **remote** is a copy of your repo hosted elsewhere. GitHub is the most common choice.  
Your local repo and GitHub stay in sync via `push` and `pull`.

```
Your machine  ──── git push ────►  GitHub
Your machine  ◄─── git pull ────   GitHub
```

---

### Step 2.1 — Create a GitHub repo

1. Go to [github.com](https://github.com) → click **New repository**
2. Name it `lif-neuron`
3. **Leave it completely empty** — no README, no .gitignore, no license
   (If you add any of those, GitHub creates a commit that conflicts with yours)
4. Copy the HTTPS URL shown on the next screen, e.g.:  
   `https://github.com/yourname/lif-neuron.git`

---

### Step 2.2 — Connect your local repo to GitHub

```bash
git remote add origin https://github.com/yourname/lif-neuron.git
```

`origin` is a nickname for that URL — you could call it anything, but `origin` is the convention.

```bash
git remote -v    # verify
```

```
origin  https://github.com/yourname/lif-neuron.git (fetch)
origin  https://github.com/yourname/lif-neuron.git (push)
```

---

### Step 2.3 — Push for the first time

```bash
git push -u origin main
```

The `-u` flag sets `origin main` as the default upstream, so from now on you can just type `git push`.

Go to your GitHub repo in the browser — all your files and commit history are there.

---

### Step 2.4 — The everyday push/pull cycle

After any local commits, push them to GitHub:

```bash
# make a change
git add simulate.py
git commit -m "Add step-input experiment"
git push
```

To pull changes made elsewhere (another machine, a collaborator, or edits made directly on GitHub):

```bash
git pull
```

> **Good habit:** `git pull` before you start working each day.

---

### ✋ Checkpoint 2

Visit your repo on GitHub. You should see:
- All 4 project files
- Your commit history under the "Commits" link
- The latest commit message next to each file

---

## Part 3 — Branches

So far everything has happened on `main`. Branches let you work on something new — a feature, an experiment, a fix — without touching the working code on `main` until you're ready.

```
main       ●────●────●────────────────────────●
                      \                      /
feature/adaptation     ●────●────●────●─────
```

Each branch is just a pointer to a commit. Switching branches is instant.

---

### Step 3.1 — Create a branch

```bash
git checkout -b feature/adaptation
```

This creates the branch and switches to it in one command. Check:

```bash
git branch       # * marks the active branch
```

```
* feature/adaptation
  main
```

---

### Step 3.2 — Make commits on the branch

**What we're adding:** spike-frequency adaptation — neurons often fire less frequently over time under constant input, due to slow K⁺ currents building up. Let's add this to the model.

Open `neuron.py` and update `__init__` and `step`:

```python
# Add to __init__:
self.adapt = 0.0          # adaptation current (nA)
self.tau_adapt = 100.0    # adaptation time constant (ms)
self.delta_adapt = 0.5    # how much each spike increases adaptation
```

```python
# In step(), in the dv calculation, subtract adaptation:
dv = (dt / self.tau_m) * (
    -(self.v - self.v_rest) + self.r_m * (i_ext - self.adapt)
)

# After detecting a spike, increment adaptation:
if spiked:
    self.adapt += self.delta_adapt

# At the end of step(), decay adaptation:
self.adapt -= (dt / self.tau_adapt) * self.adapt
```

Commit it:

```bash
git add neuron.py
git commit -m "Add spike-frequency adaptation current"
```

Now update `simulate.py` — extend the duration to 1000 ms so adaptation has time to show up:

```bash
git add simulate.py
git commit -m "Extend simulation to 1000 ms for adaptation demo"
```

Check your log:

```bash
git log --oneline --graph --all
```

```
* d4e5f6a (feature/adaptation) Extend simulation to 1000 ms for adaptation demo
* c1b2e3d Add spike-frequency adaptation current
* c3d9e1f (main) Add step-input experiment
* ...
```

---

### Step 3.3 — Push the branch to GitHub

```bash
git push -u origin feature/adaptation
```

Your branch is now on GitHub. On the repo page, use the branch dropdown to switch between `main` and `feature/adaptation` — notice `main` doesn't have your adaptation changes yet.

---

### Step 3.4 — Switch back to main

Your original code is untouched on `main`:

```bash
git checkout main
cat neuron.py   # no adaptation code here
```

This is the point of branches.

---

### ✋ Checkpoint 3

```bash
git log --oneline --graph --all
```

You should see two diverging lines of history. Your `main` is clean; `feature/adaptation` has the new commits.

---

## Part 4 — Merging

When the feature is ready, merge it back into `main`.

### Step 4.1 — Merge the branch

Make sure you're on `main`:

```bash
git checkout main
git merge feature/adaptation
```

If `main` hasn't changed since the branch was created, git does a **fast-forward** — it just moves the `main` pointer forward, no extra commit needed.

```bash
git log --oneline
```

`main` now includes all the adaptation commits.

Push the updated `main` to GitHub:

```bash
git push
```

---

### Step 4.2 — Delete the branch

Once merged, the branch is no longer needed:

```bash
git branch -d feature/adaptation              # delete locally
git push origin --delete feature/adaptation   # delete on GitHub
```

---

### Step 4.3 — Dealing with merge conflicts (simulated exercise)

Conflicts happen when the same lines were changed differently on two branches. Let's create one deliberately so you know what it looks like.

```bash
# On main, change the threshold back to -50.0
git checkout main
# edit neuron.py: v_thresh=-50.0
git add neuron.py
git commit -m "Reset threshold to -50 mV"

# Create a new branch and change it differently
git checkout -b fix/threshold
# edit neuron.py: v_thresh=-47.0
git add neuron.py
git commit -m "Experiment: lower threshold to -47 mV"

# Try to merge back
git checkout main
git merge fix/threshold
```

Git will stop and report a conflict:

```
CONFLICT (content): Merge conflict in neuron.py
Automatic merge failed; fix conflicts and then commit the result.
```

Open `neuron.py` — git has marked the conflict:

```python
<<<<<<< HEAD
        v_thresh=-50.0,   # what main has
=======
        v_thresh=-47.0,   # what fix/threshold has
>>>>>>> fix/threshold
```

To resolve:
1. Edit the file to keep what you want — delete the markers (`<<<<<<<`, `=======`, `>>>>>>>`) and the unwanted line
2. Stage the resolved file: `git add neuron.py`
3. Complete the merge: `git commit`

> **VS Code tip:** If you open the file in VS Code during a conflict, it shows  
> "Accept Current Change / Accept Incoming Change / Accept Both" buttons above each conflict.

Clean up:

```bash
git branch -d fix/threshold
git push
```

---

### ✋ Checkpoint 4

```bash
git log --oneline --graph
```

You should see a clean linear history (or a merge commit if there was a conflict). Either is fine.

---

## Part 5 — Pull Requests

On a shared project, you usually don't merge directly — you open a **pull request (PR)** so collaborators can review the code before it hits `main`.

### The PR workflow

```
1. Create branch locally
2. Push branch to GitHub          git push -u origin feature/name
3. Open a PR on GitHub            (GitHub shows a prompt automatically)
4. Collaborators review & comment
5. Push fixes to the same branch  (the PR updates automatically)
6. Approve and merge on GitHub
7. Delete the branch
```

### Try it

```bash
git checkout -b feature/readme-update
# Make a small improvement to README.md
git add README.md
git commit -m "Add usage instructions to README"
git push -u origin feature/readme-update
```

Go to your GitHub repo. You'll see a yellow banner:  
**"feature/readme-update had recent pushes — Compare & pull request"**

Click it, write a short description, and open the PR.  
Even if you're working alone, this is good practice — and GitHub's PR interface shows a clean diff of every change.

To merge: click **"Merge pull request"** on GitHub, then:

```bash
git checkout main
git pull    # bring the merge commit down to your local main
```

---

## Part 6 — Cloning (What You Could Have Done Instead)

Remember: you started this tutorial by downloading a ZIP. That meant git had no idea the files existed — you had to `git init` and rebuild the history yourself.

**Cloning** does the opposite: it downloads the repo *and* its entire history, already wired up to the remote.

```bash
git clone https://github.com/yourname/lif-neuron.git
cd lif-neuron
```

After cloning:
- `git remote -v` already shows `origin` pointing to GitHub
- `git log` shows the full commit history
- You can `pull`, `branch`, and `push` immediately

### ZIP vs Clone — when to use each

| | Download ZIP | Clone |
|---|---|---|
| Get the code to run it | ✅ | ✅ |
| Start a fresh git history | ✅ | ❌ |
| Contribute back to the project | ❌ | ✅ |
| Keep in sync with upstream changes | ❌ | ✅ |
| Share your changes via PR | ❌ | ✅ |

> The ZIP approach in this tutorial was intentional — it forced you to understand what `git init`, `remote add`, and `push` actually do. 
> In practice, if the repo already exists on GitHub, clone it.

---

## Quick Reference Card

```bash
# ── Setup ────────────────────────────────────────
git config --global user.name "Name"
git config --global user.email "email"

# ── Starting a repo ──────────────────────────────
git init                        # new local repo
git clone <url>                 # copy existing remote repo

# ── Daily workflow ────────────────────────────────
git status                      # what's changed?
git diff                        # see unstaged changes
git add <file>                  # stage a file
git add .                       # stage everything
git commit -m "message"         # commit staged changes
git log --oneline               # compact history

# ── Remote ───────────────────────────────────────
git remote add origin <url>     # connect to GitHub
git remote -v                   # check connection
git push -u origin main         # first push
git push                        # subsequent pushes
git pull                        # fetch + merge from remote
git fetch                       # fetch only (don't merge yet)

# ── Branches ─────────────────────────────────────
git branch                      # list branches
git checkout -b feature/name    # create + switch
git checkout main               # switch to main
git merge feature/name          # merge into current branch
git branch -d feature/name      # delete local branch
git push origin --delete name   # delete remote branch

# ── Undoing things ───────────────────────────────
git restore <file>              # discard unstaged changes
git restore --staged <file>     # unstage (keep changes)
git revert <hash>               # safe undo via new commit
```

---

## Commit message cheatsheet

| Type | Example |
|------|---------|
| Add something new | `Add spike-frequency adaptation` |
| Fix a bug | `Fix off-by-one in refractory period` |
| Update/improve existing | `Extend simulation to 1000 ms` |
| Remove something | `Remove unused import in plot.py` |
| Refactor | `Simplify step() logic` |

One rule: if you can't summarize the commit in one short line, it's probably too big.
