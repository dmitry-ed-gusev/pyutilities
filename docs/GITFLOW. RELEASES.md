# PYUtilities :: Git Flow. Release Policy.

[README.md](./../README.md)

[TOC]

## Git Flow

The overall git flow is represented on the picture:

![git flow](./git_flow.png){width=575 height=762}

### Git Flow step-by-step

#### Main branches

There are two major branches:

- develop - ???
- master - ???

#### Special branches

Other branches are:

- feature/xxx - ???
- release/a.b.c - ???
- hotfix/xxx - ???

#### Flow :: Release

- [develop] branch - set the release version in the [pyproject.toml](./../pyproject.toml) file, for example "2.1.0"
- create release branch [release/\<version\>], for example [release/2.1.0]
- execute integration on the release branch (should be successful)
- tag the release commit in the appropriate format: "2.1.0"
- **publish to the target**
- merge to [master] and to [develop] branches
- remove the early created release branch [release/2.1.0]

In case of any fixes for the release (before or after publishing) use the "hot-fix" approach - small hot-fix branch from the release branch, do the fix, test, merge back to the release branch, delete hot fix branch - see the next section.

#### Flow :: Hot-Fix

- step 1
- step 2
- step 3

#### Flow :: Feature/Bugfix

- step 1
- step 2
- step 3

## Release Policy

Library version is specified in the [pyproject.toml](./../pyproject.toml) file in the [project] section. 

- aaa
- bbb
- ccc
