# Ayush Sawarni — Personal Website

This repository contains the source code for my academic homepage, built with the [Minimal Light](https://github.com/yaoyao-liu/minimal-light) Jekyll theme and deployed via GitHub Pages.

## Getting Started

1. Install the Ruby toolchain along with [Bundler](https://bundler.io/).
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Serve the site locally:
   ```bash
   bundle exec jekyll serve
   ```
4. Visit <http://localhost:4000> to preview changes. Generated files live in the `_site` directory.

## Content Overview

- `index.md` — homepage content written in Markdown.
- `_includes/publications.md` — publication list embedded in the homepage.
- `_layouts/homepage.html` — layout for the landing page.
- `_sass/` — theme stylesheets for light and dark modes.
- `assets/` — static assets such as images and documents.

## Deployment

The site is automatically built and published by GitHub Pages whenever changes are pushed to the default branch. Custom domain settings are stored in the `CNAME` file.

## License

The content of this site is released under the terms specified in `LICENSE`. The underlying theme remains © the Minimal Light authors; please refer to their repository for attribution details.
