from django.test import TestCase

from apps.blog.services import calculate_reading_time, generate_blog_slug


class TestBlogServices(TestCase):
    """
    Unit tests for the business logic in services.py.
    No database access required.
    """

    def test_calculate_read_time_empty(self):
        """Should return 0 for empty content."""
        self.assertEqual(calculate_reading_time(""), 0)
        self.assertEqual(calculate_reading_time(None), 0)

    def test_calculate_read_time_short(self):
        """Should return 1 minute for short content (< 200 words)."""
        content = "word " * 50  # 50 words
        self.assertEqual(calculate_reading_time(content), 1)

    def test_calculate_read_time_long(self):
        """Should calculate correct minutes for long content."""
        # 200 words = 1 min, 400 words = 2 mins, 401 words = 3 mins (ceil)
        content = "word " * 401
        self.assertEqual(calculate_reading_time(content), 3)

    def test_slug_generation_simple(self):
        """Should standard slugify a title."""
        title = "My First Blog Post"
        self.assertEqual(generate_blog_slug(title), "my-first-blog-post")

    def test_slug_generation_special_chars(self):
        """Should handle special characters cleanly."""
        title = "Django 5.0 & React: The Ultimate Guide!"
        expected = "django-50-react-the-ultimate-guide"
        self.assertEqual(generate_blog_slug(title), expected)
