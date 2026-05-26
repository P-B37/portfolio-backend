from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.blog.models import Post

User = get_user_model()


class TestPostModel(TestCase):
    """
    Test suite for the Post model, its signals, and manager methods.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        `setUpTestData` is called once per class, making it efficient for
        creating objects that don't need to be changed in tests.
        """
        cls.user = User.objects.create_user(
            email="writer@test.com",
            password="strong-password",
        )
        cls.user2 = User.objects.create_user(
            email="anotherwriter@test.com",
            password="strong-password",
        )

    def test_post_creation_generates_slug_and_reading_time(self):
        """
        Verify that creating a post auto-generates a slug and calculates
        reading time via a pre_save signal.
        """
        post_title = "A Post About Signals"
        # Approx 250 words -> 2 minutes reading time (ceil(250/200))
        post_content = "word " * 250

        post = Post.objects.create(
            author=self.user,
            title=post_title,
            content=post_content,
        )

        # 1. Test slug generation
        self.assertEqual(post.slug, "a-post-about-signals")

        # 2. Test reading time calculation
        self.assertEqual(post.reading_time, 2)

    def test_post_creation_respects_provided_slug(self):
        """
        Verify that the pre_save signal does not overwrite a slug that is
        explicitly provided during creation.
        """
        manual_slug = "my-custom-slug"
        post = Post.objects.create(
            author=self.user,
            title="A Post with a Manual Slug",
            slug=manual_slug,
        )
        self.assertEqual(post.slug, manual_slug)

    def test_post_str_representation(self):
        """
        Test the __str__ method to ensure it returns the post's title.
        """
        post = Post(title="My Test Title")
        self.assertEqual(str(post), "My Test Title")

    def test_slug_uniqueness_enforced_by_database(self):
        """
        Verify that the database enforces the `unique=True` constraint on the
        slug field.
        """
        Post.objects.create(
            author=self.user,
            title="First Post",
            slug="shared-slug",
        )
        # Attempt to create another post with the same slug
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                author=self.user,
                title="Second Post",
                slug="shared-slug",
            )

    def test_soft_delete_and_restore(self):
        """
        Test the custom `delete` (soft delete) and `restore` methods from
        the `SoftDeleteModel` abstract class.
        """
        post = Post.objects.create(author=self.user, title="To Be Deleted")
        self.assertIn(post, Post.objects.all())

        # Soft delete the post
        post.delete()
        post.refresh_from_db()

        self.assertTrue(post.is_deleted)
        self.assertIsNotNone(post.deleted_at)
        # The default manager should no longer find it
        self.assertNotIn(post, Post.objects.all())
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(id=post.id)

        # The `all_objects` manager should still find it
        self.assertIn(post, Post.all_objects.all())

        # Restore the post
        post.restore()
        post.refresh_from_db()

        self.assertFalse(post.is_deleted)
        self.assertIsNone(post.deleted_at)
        # The default manager should find it again
        self.assertIn(post, Post.objects.all())
