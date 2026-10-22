# GitHub Pages deployment

The target is `enuminous/Devs2.0`, with public URL `https://enuminous.github.io/Devs2.0/`. Root `index.html` is a self-contained deliverable and also supports GitHub's branch-based Pages deployment when selected. The preferred workflow in `.github/workflows/verify.yml` runs software verification, the pinned Lean build and axiom audit, a computed consistency check, and a fixture integration run. It then deploys **only `_site/`** through GitHub's official Pages actions.

In repository **Settings → Pages → Build and deployment**, set Source to **GitHub Actions**. The default `github-pages` environment and repository Pages permissions must permit main-branch deployment. A successful code push does not by itself prove Pages is enabled. Inspect the workflow's deployment URL and visit it before reporting publication.

Pull requests run verification without deployment or model API calls. Main pushes and manual workflow dispatch run the same checks before deployment. Generated files must match tracked sources. All external actions are pinned to commit IDs; Lean's official Linux archive is pinned by release and SHA-256. Update those pins deliberately and rerun the complete checks.

Local development needs no build server: regenerate with `python3 scripts/build_site.py`, then open `index.html`. A simple static server can be used outside managed preview environments. The application uses relative hash navigation and works under the repository Pages prefix; there are no root-relative API paths or server-side dependencies.
