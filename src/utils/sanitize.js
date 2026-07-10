import DOMPurify from 'dompurify'

export function sanitize(html) {
  if (!html) return ''
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
      'strong', 'em', 'b', 'i', 'u', 's', 'mark', 'small',
      'ul', 'ol', 'li', 'dl', 'dt', 'dd',
      'blockquote', 'pre', 'code', 'kbd', 'samp',
      'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
      'a', 'img', 'figure', 'figcaption',
      'div', 'span', 'section', 'article', 'aside', 'header', 'footer',
      'sup', 'sub', 'abbr', 'cite', 'q',
      'iframe',
    ],
    ALLOWED_ATTR: [
      'href', 'src', 'alt', 'title', 'width', 'height',
      'class', 'id', 'style', 'target', 'rel',
      'colspan', 'rowspan', 'scope', 'align', 'valign',
      'cellpadding', 'cellspacing', 'border',
      'frameborder', 'allow', 'allowfullscreen', 'sandbox', 'loading',
    ],
    ALLOW_DATA_ATTR: false,
  })
}
