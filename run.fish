#!/usr/bin/fish

# Quick venv creator for fish sessions

set E 0
if not test -d .venv
    python -m venv .venv
    set E 1
end
source .venv/bin/activate.fish # for some reason this does not do anything, great...
if test $E -eq 1
    pip install -r requirements.txt
end