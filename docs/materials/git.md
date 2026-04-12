# git: Best Practices

Write code like you’ll have to explain it tomorrow

## Recommended Git Workflow

Work on **feature branches**, never directly on `master` (or `main`).

- Create a branch from the latest `master`: `git checkout -b feature/my-task`.
- When finished, open a Pull Request (PR) to merge it back. Skip if working alone.

The `master` branch should stay stable and linear. The only commits on `master` that have **two parents** are merge commits (they join the feature branch tip with the previous master tip). Regular commits always have one parent.

See the official workflows chapter:

- [Git Branching Workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)
- [Git Branching Basics](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging).

## Proper Commit Structure

Keep commits **small and focused** — one logical change per commit (e.g., do not mix a bug fix with a new feature in the same commit).

A good commit message has:

- First line: ≤ 50 characters, imperative mood (“Fix login crash” not “fixed crash”).
- Blank line.
- Detailed body explaining *what* changed and *why* (optional but highly recommended for non-obvious changes).

This makes commands like `git log` and `git blame` more useful, and future debugging far easier.

See also for further reading:

- [git-commit manual](https://git-scm.com/docs/git-commit)
- [Distributed Git – Contributing](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project#_commit_guidelines).

## Using Git Graphical User Interfaces (GUIs)

GUIs are excellent for visualizing branch history, seeing diffs side-by-side, and performing complex operations without typing long commands.

**Important note**: The Git integration built into most IDEs (VS Code, IntelliJ, Eclipse, etc.) is often not very user-friendly for anything beyond the simplest workflows — they hide too much and make advanced operations (rebases, cherry-picks, conflict resolution) cumbersome.

**Recommended tools** (in order of simplicity):

- Official lightweight tools (included with Git): [git-gui](https://git-scm.com/docs/git-gui) and [gitk](https://git-scm.com/docs/gitk).
- Popular full-featured standalone GUIs: GitKraken, Sourcetree, GitHub Desktop among [many others](https://git-scm.com/tools/guis).

## Resolving Conflicts

When you need to integrate changes with master, often conflicts occur, and need to be resolved. Here is a list of conflict resolution approaches in order of complexity and elegance.

When choosing a strategy — start simple, escalate only when needed.

### Merge (simplest)

`git merge other-branch`\
Git creates a merge commit. Conflicts are marked in the files; edit them or use `git mergetool`.

See [git-merge manual](https://git-scm.com/docs/git-merge) for more details.

### Cherry-picking commits one by one (selective)

Move to master branch head. Then perform `git cherry-pick <commit-hash>` for each commit you want.\
Useful when you only need specific changes from a branch. Very time-consuming if you have long list of commits.

Consider this method a manual version of the next method. Once you understand it and want to perform operations faster, consider switching.

See [git-cherry-pick manual](https://git-scm.com/docs/git-cherry-pick) for more details.

### Rebase (most powerful)

`git rebase target-branch`\
Replays your commits on top of the target. Conflicts must be resolved for each commit in sequence.

Interactive mode allows modification: reordering commits, removing them, merging commits (useful for fixes),amending commits...

See [git-rebase manual](https://git-scm.com/docs/git-rebase) for more details.

## Pull Requests and the Approval System

For teamwork:

- Push your feature branch to the remote repository.
- Open a **Pull Request** (PR) on GitHub, GitLab, or similar.
- Other developers review the changes and leave comments.
- Once the PR has the required number of approvals, it can be merged (usually via the web interface).

This workflow enforces code review and keeps `master` clean. Never merge your own PR without at least one approval from the team (follow your project’s rules).

See your hosting platform’s documentation (GitHub PRs, GitLab Merge Requests).\
Git itself provides `git request-pull` for email-based reviews if you are not using a web platform:\
[git-request-pull](https://git-scm.com/docs/git-request-pull).

## Obscure but Useful Operations

**git format-patch / git am**

- `git format-patch <range>` → creates patch files (`.patch`) from a range of commits.
- `git am <file.patch>` → applies those patches cleanly (preserves author, date, etc.).\
  Perfect for sending changes by email or applying patches from mailing lists.

**git bisect**\
Binary-search tool that finds the exact commit that introduced a bug.\
You mark a known-good and known-bad commit; Git checks out commits in the middle and you tell it “good” or “bad” until the culprit is isolated.

## Further reading

- [Official Git reference](https://git-scm.com/docs).
- [Free book Pro Git](https://git-scm.com/book/en/v2).
- [Pro Git – Basic Merge Conflicts](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merge_conflicts).
