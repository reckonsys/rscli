# rscli

Reckonsys CLI toolchain

## Who is this for?

`rscli` is an internal toolchain that we use here at Reckonsys to manage our workflows. If you are not an employee at Reckonsys, this tool may not make any sense to you.


## What will it do?

* Scaffolds out project
* Adds `.gitginore`
* Adds `.infra.json`
* Adds `guniconfig.py` (For python projects)
* Adds `yarn build:<env>` (For node projects)

## Completion

source <(inv --print-completion-script bash)
