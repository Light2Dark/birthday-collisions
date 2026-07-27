# Birthday Collisions

An interactive marimo notebook about the birthday paradox.

## Live app

**https://light2dark.github.io/birthday-collisions/**

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/Light2Dark/birthday-collisions/blob/main/custom.py/wasm)

## Local development

```bash
uvx marimo edit custom.py
```

## Export (html-wasm, run mode, show code)

```bash
uvx --from 'marimo>=0.23.15' marimo export html-wasm custom.py \
  -o _site \
  --mode run \
  --show-code \
  --sandbox \
  -f

python -m http.server --directory _site
```

Pushes to `main` rebuild and publish via GitHub Actions ([docs](https://docs.marimo.io/guides/publishing/github/#publish-using-github-actions)).
