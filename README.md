# Personal website for Ayush Sawarni

This repository contains the source for Ayush Sawarni’s academic homepage. The site is a minimal single page built with [Jekyll](https://jekyllrb.com/) that keeps content in Markdown and BibTeX files so updates stay lightweight.

## Getting started

1. **Install dependencies**

   ```bash
   bundle install
   ```

2. **Serve the site locally**

   ```bash
   bundle exec jekyll serve
   ```

   The site is available at <http://localhost:4000>. Changes to Markdown, HTML, CSS, or JavaScript files trigger an automatic rebuild.

## Updating content

### Profile & metadata

Edit [`_config.yml`](./_config.yml) to change your name, role, institution, bio snippet, and social links. The header and contact footer read directly from these values.

### Homepage sections

[`index.md`](./index.md) is regular Markdown. Update the headings or lists to change the “About”, “Research interests”, “Open problems”, and “Service” sections without touching the layout.

### Publications from BibTeX

Add or edit entries in [`assets/data/references.bib`](assets/data/references.bib). Supported fields include:

| Field       | Purpose                                               |
|-------------|-------------------------------------------------------|
| `title`     | Display title (required)                              |
| `author`    | Author list (separate names with `and`)               |
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

- The author that matches `primary_author` (defaults to `site.name`) is rendered in **bold**.
- Include `alphabetical` in `keywords` to add an “Alphabetical Authors” badge.
- Include `spotlight`, `oral`, or `talk` in `keywords` to surface presentation highlights alongside any custom `note` text.

## Assets

Profile and favicon images live in [`assets/img/`](assets/img/). Replace them with files of the same name or update the paths in `_config.yml`.

## Deployment

The project works with GitHub Pages. Push the branch configured for your Pages site and GitHub will rebuild automatically using the included configuration.

## License

Content is © Ayush Sawarni. Templates and build configuration are provided under the MIT License.
