from django.test import TestCase
from apps.projects.models import Project, Status


class ProjectManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        # Create a user for the projects
        cls.p1 = Project.objects.create(
            title="Published and Featured",
            status=Status.PUBLISHED,
            is_featured=True,
            summary="summary",
            content="content",
        )
        cls.p2 = Project.objects.create(
            title="Published Not Featured",
            status=Status.PUBLISHED,
            is_featured=False,
            summary="summary",
            content="content",
        )
        cls.p3 = Project.objects.create(
            title="Draft Project",
            status=Status.DRAFT,
            summary="summary",
            content="content",
        )
        cls.p4 = Project.objects.create(
            title="Archived Project",
            status=Status.ARCHIVED,
            summary="summary",
            content="content",
        )
        cls.p5 = Project.objects.create(
            title="Deleted Project",
            status=Status.PUBLISHED,
            is_deleted=True,
            summary="summary",
            content="content",
        )

    def test_published_manager_method(self):
        """
        Test that the `published` manager method
        returns only published projects.
        """

        published_projects = Project.objects.published()
        self.assertEqual(published_projects.count(), 2)
        self.assertIn(self.p1, published_projects)
        self.assertIn(self.p2, published_projects)
        self.assertNotIn(self.p3, published_projects)
        self.assertNotIn(self.p4, published_projects)
        self.assertNotIn(self.p5, published_projects)

    def test_featured_manager_method(self):
        """
        Test that the `featured` manager
        method returns only featured projects.
        """

        featured_projects = Project.objects.featured()
        self.assertEqual(featured_projects.count(), 1)
        self.assertIn(self.p1, featured_projects)
        self.assertNotIn(self.p2, featured_projects)
        self.assertNotIn(self.p3, featured_projects)
        self.assertNotIn(self.p4, featured_projects)
        self.assertNotIn(self.p5, featured_projects)

    def test_chaining_manager_methods(self):
        """
        Test that manager methods can be chained together.
        """

        featured_and_published = Project.objects.published().featured()
        self.assertEqual(featured_and_published.count(), 1)
        self.assertIn(self.p1, featured_and_published)

        # Also test the other way around
        published_and_featured = Project.objects.featured().published()
        self.assertEqual(published_and_featured.count(), 1)
        self.assertIn(self.p1, published_and_featured)

    def test_soft_delete_exclusion(self):
        """
        Test that soft-deleted projects
        are excluded from the default manager.
        """

        all_projects = Project.objects.all()
        self.assertEqual(all_projects.count(), 4)
        self.assertNotIn(self.p5, all_projects)

    def test_empty_queryset_for_no_results(self):
        """
        Test that an empty queryset is
        returned when no projects match.
        """

        Project.objects.all().delete()
        self.assertEqual(Project.objects.all().count(), 0)
        self.assertEqual(Project.objects.published().count(), 0)
        self.assertEqual(Project.objects.featured().count(), 0)
