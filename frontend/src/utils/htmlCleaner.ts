/**
 * Sanitizes HTML string and returns an object for dangerouslySetInnerHTML
 * @param html - The HTML string to sanitize
 * @returns Object with __html property for React's dangerouslySetInnerHTML
 */
export function cleanHtml(html: string | null | undefined): { __html: string } {
    if (!html) return { __html: '' };

    // Create a temporary div element to parse and sanitize HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;

    // Return the sanitized HTML
    return { __html: tempDiv.innerHTML };
}

/**
 * Strips HTML tags from a string and returns plain text
 * @param html - The HTML string to clean
 * @returns Plain text without HTML tags
 */
export function stripHtml(html: string | null | undefined): string {
    if (!html) return '';

    // Create a temporary div element to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;

    // Get text content (automatically strips tags)
    let text = tempDiv.textContent || tempDiv.innerText || '';

    // Clean up extra whitespace and line breaks
    text = text.replace(/\s+/g, ' ').trim();

    return text;
}