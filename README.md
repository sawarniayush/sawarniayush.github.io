# Personal website for Ayush Sawarni

This repository contains the source for Ayush Sawarni’s academic homepage. The site is built with [Jekyll](https://jekyllrb.com/) and renders a single-page profile that automatically loads publications from a BibTeX file.

## Key features

- Modern, single-page layout with responsive navigation and built-in contact section.
- Publications and writing samples are generated automatically from [`assets/data/references.bib`](assets/data/references.bib).
- Simple configuration through [`_config.yml`](./_config.yml) for profile details and social links.
- Accessible defaults (skip links, keyboard-friendly navigation, reduced-motion support).

## Getting started

1. **Install dependencies**

   ```bash
   bundle install
   ```

2. **Serve the site locally**

   ```bash
   bundle exec jekyll serve
   ```

   The site will be available at <http://localhost:4000>. Changes to Markdown, HTML, CSS, or JavaScript files will trigger a rebuild.

## Updating content

### Profile & links

Edit [`_config.yml`](./_config.yml) to update your name, role, institution, bio, and social links. The hero section and footer read directly from these values.

### Homepage sections

[`index.md`](./index.md) uses regular Markdown. Update headings, paragraphs, and bullet lists to customise the “Research focus”, “Research interests”, and other sections.

### Publications via BibTeX

Add, edit, or remove entries in [`assets/data/references.bib`](assets/data/references.bib). Each entry supports the following fields:

| Field       | Purpose                                               |
|-------------|-------------------------------------------------------|
| `title`     | Display title (required)                              |
| `author`    | Author list (use `and` between authors)               |
| `booktitle` | Venue for conference or workshop papers               |
| `journal`   | Venue for journal papers                              |
| `year`      | Year of publication (used for sorting)                |
| `url`       | Primary link for the paper                            |
| `pdf`       | Direct link to the PDF (optional)                     |
| `code`      | Link to a code repository (optional)                  |
| `slides`    | Slide deck link (optional)                            |
| `talk`      | Recording or talk link (optional)                     |
| `poster`    | Poster link (optional)                                |
| `keywords`  | Comma-separated badges such as `spotlight`, `oral`, `talk`, or `alphabetical` |
| `note`      | Additional free-form note text                        |

Special handling:

- **Primary author highlighting** – the author that matches `primary_author` (defaults to `site.name`) is automatically bolded.
- **Alphabetical author lists** – include `alphabetical` in `keywords` to add a badge noting the ordering.
- **Event spotlights** – include `spotlight`, `oral`, or `talk` in `keywords` to surface presentation highlights.

### Images

Profile and favicon images live in [`assets/img/`](assets/img/). Replace them with files of the same name or update the paths in `_config.yml`.

## Deployment

This site is compatible with GitHub Pages. The `github-pages` gem pins the same dependencies that GitHub uses, so the build locally should match the published output. Push changes to the `main` branch (or the branch configured in your repository settings) and GitHub Pages will rebuild the site automatically.

## License

The content in this repository is © Ayush Sawarni. The build configuration and templates are available under the MIT License.
