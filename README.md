# Notes

These are some notes I want to keep around.

# Setup

```
git clone git@github.com:Sarcasm/notes.git
cd notes
git fetch origin gh-pages
git checkout gh-pages
git checkout master
git worktree add --checkout _pages gh-pages
# configure `git push` to push both branches
git config remote.origin.push refs/heads/master:refs/heads/master
git config --add remote.origin.push refs/heads/gh-pages:refs/heads/gh-pages
```

# Publish changes

After a change has been committed to the main branch, it's possible to publish
using this procedure:

```
make _pages
./commit-pages.sh
git push
```
