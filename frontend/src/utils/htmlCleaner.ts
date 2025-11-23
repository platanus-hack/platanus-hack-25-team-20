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