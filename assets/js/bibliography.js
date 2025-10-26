(function () {
  const container = document.getElementById('publications-list');
  if (!container) return;

  const bibliographyPath = container.dataset.bibliography || 'assets/data/references.bib';
  const primaryAuthor = container.dataset.primaryAuthor || '';

  function parseBibtex(text) {
    const entries = [];
    const cleaned = text.replace(/%.*$/gm, '').trim();
    const regex = /@([a-zA-Z]+)\s*\{([^,]+),([\s\S]*?)\n\}/g;
    let match;
    while ((match = regex.exec(cleaned)) !== null) {
      const type = match[1].trim();
      const key = match[2].trim();
      const body = match[3].trim();
      const tags = {};
      let index = 0;
      while (index < body.length) {
        while (index < body.length && /[\s,]/.test(body[index])) index += 1;
        if (index >= body.length) break;
        let keyStart = index;
        while (index < body.length && /[^\s=]/.test(body[index])) index += 1;
        const fieldName = body.slice(keyStart, index).trim().toLowerCase();
        while (index < body.length && /[\s=]/.test(body[index])) index += 1;
        if (index >= body.length) break;
        let value = '';
        if (body[index] === '{') {
          let depth = 0;
          index += 1;
          const start = index;
          while (index < body.length) {
            if (body[index] === '{') depth += 1;
            else if (body[index] === '}') {
              if (depth === 0) break;
              depth -= 1;
            }
            index += 1;
          }
          value = body.slice(start, index).trim();
          index += 1;
        } else if (body[index] === '"') {
          index += 1;
          const start = index;
          while (index < body.length && body[index] !== '"') index += 1;
          value = body.slice(start, index).trim();
          index += 1;
        } else {
          const start = index;
          while (index < body.length && /[^,\s]/.test(body[index])) index += 1;
          value = body.slice(start, index).trim();
        }
        tags[fieldName] = value;
      }
      entries.push({ type, key, tags });
    }
    return entries;
  }

  function toTitleCase(str) {
    return str
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  function formatAuthors(authorField) {
    if (!authorField) return '';
    const authors = authorField.split(/\s+and\s+/i).map((name) => name.trim());
    return authors
      .map((author) => {
        const cleanAuthor = author.replace(/\s+/g, ' ').trim();
        if (!primaryAuthor) return cleanAuthor;
        const pattern = new RegExp(primaryAuthor, 'i');
        return pattern.test(cleanAuthor) ? `<strong>${cleanAuthor}</strong>` : cleanAuthor;
      })
      .join(', ');
  }

  function buildLink(label, url) {
    if (!url) return '';
    return `<a href="${url}" target="_blank" rel="noopener">${label}</a>`;
  }

  function createTag(label) {
    return `<span class="tag">${label}</span>`;
  }

  function normaliseKeywords(raw) {
    if (!raw) return [];
    return raw
      .split(/[,;]+/)
      .map((word) => word.trim().toLowerCase())
      .filter(Boolean);
  }

  function render(entries) {
    if (!entries.length) {
      container.innerHTML = '<p>No publications found. Update your BibTeX file to see entries here.</p>';
      return;
    }

    const yearValue = (tags) => parseInt(tags.year, 10) || 0;
    const monthValue = (tags) => {
      if (!tags.month) return 0;
      const monthNames = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
      ];
      const normalised = tags.month.toLowerCase().slice(0, 3);
      const index = monthNames.indexOf(normalised);
      return index === -1 ? 0 : index + 1;
    };

    entries.sort((a, b) => {
      const yearDiff = yearValue(b.tags) - yearValue(a.tags);
      if (yearDiff !== 0) return yearDiff;
      return monthValue(b.tags) - monthValue(a.tags);
    });

    const cards = entries.map(({ tags }) => {
      const title = tags.title || tags.booktitle || tags.journal || 'Untitled';
      const authors = formatAuthors(tags.author);
      const venue = tags.booktitle || tags.journal || tags.school || tags.howpublished || '';
      const year = tags.year ? `${tags.year}` : '';
      const venueLine = [venue && `<em>${venue}</em>`, year].filter(Boolean).join(' · ');

      const links = [
        buildLink('Paper', tags.url || tags.link || tags.pdf),
        buildLink('PDF', tags.pdf && tags.pdf !== tags.url ? tags.pdf : ''),
        buildLink('Code', tags.code),
        buildLink('Slides', tags.slides),
        buildLink('Talk', tags.talk || tags.video),
        buildLink('Poster', tags.poster)
      ].filter(Boolean);

      const keywords = normaliseKeywords(tags.keywords);
      const badges = keywords
        .filter((keyword) => keyword !== 'alphabetical')
        .map((keyword) => createTag(toTitleCase(keyword)));

      if (keywords.includes('alphabetical')) {
        badges.push(createTag('Alphabetical Authors'));
      }

      const note = [];
      if (keywords.includes('spotlight')) note.push('Spotlight presentation');
      if (keywords.includes('oral')) note.push('Oral presentation');
      if (keywords.includes('talk')) note.push('Talk');
      if (tags.note) note.push(tags.note);

      const spotlightText = note.length ? `<p class="publication-card__note">${note.join(' · ')}</p>` : '';
      const linkMarkup = links.length
        ? `<div class="publication-card__links">${links.map((link) => `<span>${link}</span>`).join('')}</div>`
        : '';
      const badgeMarkup = badges.length
        ? `<div class="publication-card__tags">${badges.join('')}</div>`
        : '';

      const titleLink = tags.url || tags.link || tags.pdf || '#';
      const safeTitle = title.replace(/\{\}/g, '');

      return `
        <article class="publication-card">
          <h3 class="publication-card__title"><a href="${titleLink}" target="_blank" rel="noopener">${safeTitle}</a></h3>
          ${venueLine ? `<p class="publication-card__meta">${venueLine}</p>` : ''}
          ${authors ? `<p class="publication-card__authors">${authors}</p>` : ''}
          ${badgeMarkup}
          ${linkMarkup}
          ${spotlightText}
        </article>
      `;
    });

    container.innerHTML = cards.join('');
  }

  fetch(bibliographyPath)
    .then((response) => {
      if (!response.ok) throw new Error('Unable to load bibliography');
      return response.text();
    })
    .then((text) => {
      const entries = parseBibtex(text);
      render(entries);
    })
    .catch(() => {
      container.innerHTML = '<p>Unable to load publications right now. Please try again later.</p>';
    });
})();
