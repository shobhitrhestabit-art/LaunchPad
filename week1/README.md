#  Week 1 — Lessons Learned & What Broke

Week 1 was a deep dive into understanding Git workflows, command-line fundamentals, debugging techniques, and project structuring. Throughout the week, I explored important concepts by breaking things on purpose—and sometimes by accident—which helped reinforce real-world problem-solving skills.

##  Lessons Learned
1. Git Commit Discipline Matters

I learned the importance of making small, meaningful commits. Each commit should reflect a logical unit of work. This makes debugging easier and provides a clean project history.

2. Understanding Git Bisect

Using git bisect taught me how powerful binary search is for debugging. Instead of manually checking each commit, bisect quickly narrowed down the exact commit where the bug was introduced.

3. Reverting Without Rewriting History

I learned how git revert is safer than git reset when working in a shared repository. Revert preserves history by adding a new commit that undoes the changes from a faulty commit.

4. The Stash Workflow

git stash, git pull, and git stash apply helped me understand how to temporarily save work-in-progress without committing. Stashing is especially useful when switching branches or pulling new updates.

5. Merge Conflicts Are Normal

Instead of fearing merge conflicts, I now understand how and why they occur. I learned how to resolve them using VS Code’s conflict resolution tool and how to merge while keeping both changes when required.

6. Using Two Clones to Simulate Team Collaboration

Working with two clones helped me experience real-world scenarios where multiple developers work on the same file. It showed how communication and proper workflow prevent bigger issues.

## What Broke (And How I Fixed It)
1. Merge Conflicts Everywhere

While practicing merges, I repeatedly ran into conflicts—especially when editing the same line from two different clones. This helped me understand conflict markers, conflict resolution options, and how merge commits are created.

2. Stash Didn’t Work at First

I tried stashing a new .txt file and nothing happened. I later learned that Git does not stash untracked files unless you use git stash -u or track the file first.

3. Accidentally Merging the Wrong Branch

At one point, I merged main into main, which obviously caused no conflict and confused me. I learned the importance of confirming which branch I’m on using git branch or git status before merging.

4. Broken Feature Commit (Intentional Bug)

I introduced a bug in commit #4, which temporarily broke my app. This was intentional, but it taught me how to use bisect to isolate the buggy commit and how revert can “undo” a commit safely.

5. Pull Failing Because of Local Changes

At times git pull failed because untracked or modified files were preventing a clean merge. This taught me when to stash, when to commit, and when to delete unneeded files.

## Week 1 Summary

Week 1 was full of experiments, mistakes, debugging, and learning. Breaking things intentionally helped build confidence in using Git correctly. By understanding commit discipline, bisect, revert, stash workflows, and merge conflict resolution, I now have a stronger foundation for real-world Git-based development.