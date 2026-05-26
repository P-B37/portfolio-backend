from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.blog.models import Post, StatusChoices

User = get_user_model()


class TestPostManager(TestCase):
    """
    Integration tests for PostManager query logic.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="author@test.com", password="password1234"
        )
        cls.another_user = User.objects.create_user(
            email="another@test.com", password="password1234"
        )

        cls.post_1 = Post.objects.create(
            author=cls.user,
            title="Published Post",
            status=StatusChoices.PUBLISHED,
            content="# Content of published post.",
        )

        cls.post_2 = Post.objects.create(
            author=cls.user,
            title="Draft Post",
            status=StatusChoices.DRAFT,
            content="# Content of draft post.",
        )

        cls.post_3 = Post.objects.create(
            author=cls.user,
            title="Archived Post",
            status=StatusChoices.ARCHIVED,
            content="# Content of Archived post.",
        )

        cls.post_4 = Post.objects.create(
            author=cls.another_user,
            title="Another User's Post",
            status=StatusChoices.PUBLISHED,
            content="# Content of another user's post.",
        )

    def test_published_manager_filters_drafts_and_archived(self):
        """The .published() method should exclude drafts."""
        queryset = Post.objects.published()

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.post_1, queryset)
        self.assertNotIn(self.post_2, queryset)
        self.assertNotIn(self.post_3, queryset)

    def test_by_author_manager_filters_correctly(self):
        """The .by_author() method should return posts only by the specified author."""

        queryset = Post.objects.by_author(self.user)

        self.assertEqual(queryset.count(), 3)
        self.assertIn(self.post_1, queryset)
        self.assertIn(self.post_2, queryset)
        self.assertIn(self.post_3, queryset)
        self.assertNotIn(self.post_4, queryset)
        self.assertIn(self.post_4, Post.objects.by_author(self.another_user))

    def test_manager_excludes_soft_deleted(self):
        """The default manager should hide soft-deleted posts."""
        self.post_1.delete()  # Trigger soft delete

        # Standard objects.all() should be empty due to custom get_queryset
        self.assertEqual(Post.objects.all().count(), 3)

        # But it should still exist in DB (Hard verification)
        # We bypass the manager using _base_manager or raw SQL check concept
        self.assertEqual(Post.all_objects.count(), 4)
