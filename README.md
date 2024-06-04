[![progress-banner](https://backend.codecrafters.io/progress/git/a7081418-c793-4c95-901b-f6d2546bb97e)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Git" Challenge](https://codecrafters.io/challenges/git).

In this challenge, you'll build a small Git implementation that's capable of
initializing a repository, creating commits and cloning a public repository.
Along the way we'll learn about the `.git` directory, Git objects (blobs,
commits, trees etc.), Git's transfer protocols and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your Git implementation is in `app/main.py`. Study and
uncomment the relevant code, and push your changes to pass the first stage:

```sh
git add .
git commit -m "pass 1st stage" # any msg
git push origin master
```

That's all!

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `python` installed locally
1. Run `./your_git.sh` to run your Git implementation, which is implemented in
   `app/main.py`.
1. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.

# Testing locally

The `your_git.sh` script is expected to operate on the `.git` folder inside the
current working directory. If you're running this inside the root of this
repository, you might end up accidentally damaging your repository's `.git`
folder.

We suggest executing `your_git.sh` in a different folder when testing locally.
For example:

```sh
mkdir -p /tmp/testing && cd /tmp/testing
/path/to/your/repo/your_git.sh init
```

To make this easier to type out, you could add a
[shell alias](https://shapeshed.com/unix-alias/):

```sh
alias mygit=/path/to/your/repo/your_git.sh

mkdir -p /tmp/testing && cd /tmp/testing
mygit init
```

A commit object contains information like:

Committer/Author name + email
Timestamp
Tree SHA
Parent commit SHA(s), if any

# Create a new directory and cd into it

$ mkdir test_dir && cd test_dir

# Initialize a new git repository

$ git init
Initialized empty Git repository in /path/to/test_dir/.git/

# Create a tree, get its SHA

$ echo "hello world" > test.txt
$ git add test.txt
$ git write-tree
4b825dc642cb6eb9a060e54bf8d69288fbee4904

# Create the initial commit

$ git commit-tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904 -m "Initial commit"
3b18e512dba79e4c8300dd08aeb37f8e728b8dad

# Write some changes, get another tree SHA

$ echo "hello world 2" > test.txt
$ git add test.txt
$ git write-tree
5b825dc642cb6eb9a060e54bf8d69288fbee4904

# Create a new commit with the new tree SHA

$ git commit-tree 5b825dc642cb6eb9a060e54bf8d69288fbee4904 -p 3b18e512dba79e4c8300dd08aeb37f8e728b8dad -m "Second commit"
