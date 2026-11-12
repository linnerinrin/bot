import re


def get_url_from_cq(cq_str,searchs):
    match = re.search(searchs, cq_str)
    if match:
        url = match.group(1)
        url = url.replace("&amp;", "&")
        return url
    return None