from bs4 import BeautifulSoup

def extract_medium_article(soup: BeautifulSoup):
    """
    Extracts the main content from a Medium article soup object.
    Returns the main HTML block as a string.
    """
    main_block = soup.find('article') or soup.find('section', class_='pw-post-body')
    # Remove clap button, author info, recommended articles sections
    for tag in soup.find_all(class_=lambda x: x and ('postActions' in x or 'authorInfo' in x or 'recommendedPosts' in x)):
        tag.decompose()
    if not main_block:
        main_block = soup.find('div', class_='section-content') or soup.find('div', class_='section-inner')
    if not main_block:
        for section in soup.find_all(['section', 'div']):
            if section.find(['h1', 'h2', 'h3']) and section.find(['p']):
                main_block = section
                break
    if main_block:
        headers = []
        for h in main_block.find_all(['h1', 'h2', 'h3']):
            header_text = h.get_text().strip()
            if header_text in headers:
                h.decompose()
            else:
                headers.append(header_text)
        return str(main_block)
    return ""

def extract_generic_content(soup: BeautifulSoup):
    """
    Extracts the main content from a generic site soup object.
    Returns the main HTML block as a string.
    """
    selectors = [
        ("div", {"id": "mw-content-text"}),
        ("div", {"id": "bodyContent"}),
        ("article", {}),
        ("main", {}),
        ("div", {"id": "content"}),
        ("div", {"class_": "content"}),
        ("div", {"class_": "post-content"}),
        ("div", {"class_": "entry-content"}),
        ("div", {"itemprop": "articleBody"}),
        ("section", {}),
    ]
    main_block = None
    for name, attrs in selectors:
        main_block = soup.find(name, attrs)
        if main_block:
            break
    if not main_block:
        best_container = None
        max_p_count = 0
        for container in soup.find_all(['article', 'div', 'section']):
            p_count = len(container.find_all('p'))
            if p_count > max_p_count:
                max_p_count = p_count
                best_container = container
        if best_container:
            main_block = best_container
    if not main_block:
        content_tags = []
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table", "blockquote", "pre", "code"]:
            content_tags.extend(soup.find_all(tag))
        if content_tags:
            wrapper = soup.new_tag("div")
            for tag in content_tags:
                wrapper.append(tag)
            main_block = wrapper
    if not main_block:
        body = soup.body
        if body:
            return body.get_text(separator="\n", strip=True)
        return ""
    return str(main_block)

def extract_wikipedia_article(soup):
    """
    Extracts the main content from a Wikipedia article soup object.
    Returns the main HTML block as a string.
    """
    main_block = soup.find("div", {"id": "mw-content-text"})
    if main_block:
        # Remove edit sections, reference lists, navigation boxes
        for edit_section in main_block.find_all("span", class_="mw-editsection"):
            edit_section.decompose()
        for ref_list in main_block.find_all("div", class_="reflist"):
            ref_list.decompose()
        for nav in main_block.find_all("div", class_="navbox"):
            nav.decompose()
        # Extract only visible text and key content tags
        content_tags = []
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table", "blockquote", "pre", "code"]:
            content_tags.extend(main_block.find_all(tag))
        if content_tags:
            wrapper = soup.new_tag("div")
            for tag in content_tags:
                wrapper.append(tag)
            return str(wrapper)
        return str(main_block)
    # Fallback: return all text if main block not found
    body = soup.body
    if body:
        return body.get_text(separator="\n", strip=True)
    return ""
