import math
from django.utils.text import slugify


def generate_blog_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from the blog title.
    """
    return slugify(title)


def calculate_reading_time(content: str) -> int:
    """
    Estimate the reading time for the blog content in minutes.
    Assumes an average reading speed of 200 words per minute.
    """
    if not content:
        return 0
    word_count = len(content.split())
    reading_time = math.ceil(word_count / 200)
    return reading_time
