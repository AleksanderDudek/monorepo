You are generating a single-page marketing website for a Polish small business.

Output STRICT JSON with exactly two keys: "html" and "css". No markdown
fences, no commentary, no preamble. The JSON must be parseable directly.

Constraints:
- The HTML must be a complete document (<!doctype html>...</html>).
- It must link to "styles.css" for all styling. No inline <style> tags.
- No external CSS frameworks. No JavaScript. No external fonts beyond
  system fonts unless absolutely needed.
- All copy in natural Polish, written as the business owner would write it.
- Mobile-first responsive layout.
- Sections: hero, 3 value props, about, services/offer, contact, footer.
- Include the provided phone and email in the contact section if present.
- Tasteful, modern, neutral design that suits the industry.
- No placeholder text like "Lorem ipsum" or "[Your text here]".
- No fake testimonials. If a testimonials block helps the design,
  mark it visually as "Miejsce na opinie klientów".

Business details:
- Name: {name}
- NIP: {nip}
- Existing website: {url_or_none}
- Email: {email_or_none}
- Phone: {phone_or_none}
- Industry (PKD): {pkd_or_none}
- Additional context: {notes_or_none}

Return only the JSON object.
