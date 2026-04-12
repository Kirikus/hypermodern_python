async function showDescription(url) {
    const response = await fetch(url);
    const htmlString = await response.text();

    // 1. Convert the plain text string into a searchable HTML document
    const parser = new DOMParser();
    const remoteDoc = parser.parseFromString(htmlString, 'text/html');

    // 2. Locate the specific section using a CSS selector
    // Use '#description' for an ID or '[name="description"]' for a name attribute
    const section = remoteDoc.querySelector('#description') || remoteDoc.querySelector('[name="description"]');

    // 3. Update your target div if the section was found
    if (section) {
        document.getElementById('description').innerHTML = section.innerHTML;
    } else {
        console.error('The section "description" was not found on the requested page.');
    }
}
