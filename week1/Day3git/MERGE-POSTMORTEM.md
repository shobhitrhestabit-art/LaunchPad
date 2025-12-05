
# MERGE-POSTMORTEM

# Merge Conflict Report

This report explains how a merge conflict was intentionally created, how the issue occurred, and how it was resolved using Git and VS Code. All steps are written in clear Markdown syntax for documentation purposes.


## 1. Creating the Merge Conflict Scenario

To demonstrate a merge conflict, two branches were used: main and features.
Both branches contained a shared file named app.txt.
A conflict was prepared by modifying the same line (Line 3) differently in each branch.

In the main branch, Line 3 was changed to reflect one version of the update.

In the features branch, Line 3 was changed again but with different wording.

Because both branches edit the same section differently, Git cannot automatically select which version to keep when merging.



## Screenshots

![App Screenshot](https://raw.githubusercontent.com/shobhitrhestabit-art/Day3-git/main/SS.png
)



## 🟦 2. How the Merge Conflict Occurred

After the conflicting changes were made on both branches, the features branch attempted to merge the main branch into it.
During the merge, Git detected that both branches modified the exact same line in app.txt.

Since Git cannot resolve this type of conflict automatically, it stopped the merge and marked the file as conflicted.
The file temporarily displayed Git’s conflict markers:






## 🟦 3. Resolving the Merge Conflict

The conflict was resolved inside VS Code, which provides built-in merge tools.
When the conflicting file was opened, VS Code displayed options such as:

Accept Current Change

Accept Incoming Change

Accept Both Changes

Compare Changes

As required by the task, the option “Accept Both Changes” was selected.
This retained both versions from the main and features branches.

After resolving the conflict:

The file was cleaned by removing conflict markers.

The updated file was saved.

The merge was completed by staging the file and committing the resolution.



## Screenshots

![App Screenshot](https://raw.githubusercontent.com/shobhitrhestabit-art/Day3-git/main/mergeConflcit.png
)



## 🟦 4. Final Result

The merge conflict was successfully resolved, and both changes were preserved.
The features branch now contains:

The original features branch content

The incoming changes from the main branch

A merge commit documenting the resolution

This demonstrates a full real-world workflow of handling merge conflicts in Git — from creation, to identification, to successful resolution.

![Merge Graph](https://raw.githubusercontent.com/shobhitrhestabit-art/Day3-git/main/Graphmerging.png)

