from django.test import TestCase

from apps.projects.models import Project
from apps.projects.services import generate_project_slug


class ProjectModelSignalTests(TestCase):
    """
    Test suite for signals related to the Project model.
    """

    def test_slug_is_generated_on_creation(self):
        """
        Test that a slug is automatically generated
        when a new Project is created.
        """
        project = Project.objects.create(title="New Project", summary="s", content="c")
        self.assertIsNotNone(project.slug)
        self.assertNotEqual(project.slug, "")

        expected_slug = generate_project_slug(project.title, project.id)
        self.assertEqual(project.slug, expected_slug)

    def test_slug_is_not_overwritten_on_update(self):
        """
        Test that the slug is not changed when
        an existing Project is updated.
        """
        project = Project.objects.create(
            title="Original Title", summary="s", content="c"
        )
        original_slug = project.slug

        project.title = "Updated Title"
        project.save()

        self.assertEqual(project.slug, original_slug)

    def test_manual_slug_is_preserved(self):
        """
        Test that a manually provided slug is not overwritten.
        """
        manual_slug = "this-is-a-manual-slug"
        project = Project.objects.create(
            title="Test Project", slug=manual_slug, summary="s", content="c"
        )
        self.assertEqual(project.slug, manual_slug)

    def test_slug_behavior_on_save_without_mock(self):
        """
        Tests the slug generation logic by observing the state of the slug
        field under different conditions, without using mocks.
        """
        # Scenario 1: Test that slug is generated on initial creation
        project1 = Project.objects.create(
            title="First Project", summary="s", content="c"
        )
        expected_slug = generate_project_slug(project1.title, project1.id)
        self.assertEqual(project1.slug, expected_slug)
        self.assertTrue(project1.slug)  # Verify it's not empty

        # Store original slug for the next step
        original_slug = project1.slug

        # Scenario 2: Test that the slug is NOT regenerated on update
        project1.title = "An Updated Title"
        project1.save()
        self.assertEqual(project1.slug, original_slug)  # Should not have changed

        # Scenario 3: Test that a manually provided slug is preserved
        manual_slug = "my-own-slug"
        project2 = Project.objects.create(
            title="Second Project", slug=manual_slug, summary="s", content="c"
        )
        self.assertEqual(project2.slug, manual_slug)
