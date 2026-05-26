from uuid import uuid4

import pytest

from apps.projects.services import generate_project_slug


@pytest.mark.parametrize(
    "title, project_id, expected_slug_part",
    [
        ("My Test Project", str(uuid4()), "my-test-project"),
        ("My Test Project!@#", str(uuid4()), "my-test-project"),
        (
            "  Leading and Trailing Spaces  ",
            str(uuid4()),
            "leading-and-trailing-spaces",
        ),
        ("russkii proekt", str(uuid4()), "russkii-proekt"),
        ("puroziekuto", str(uuid4()), "puroziekuto"),
        ("a" * 60, str(uuid4()), "a" * 60),
    ],
)
def test_generate_project_slug_various_titles(title, project_id, expected_slug_part):
    """
    Test generate_project_slug with various titles to ensure correct slugification.
    """
    short_id = project_id[:8]
    expected_slug = f"{expected_slug_part}-{short_id}"
    slug = generate_project_slug(title, project_id)
    assert slug == expected_slug


def test_generate_project_slug_idempotency():
    """
    Test that generate_project_slug is idempotent.
    """
    project_id = str(uuid4())
    title = "Idempotency Test"
    slug1 = generate_project_slug(title, project_id)
    slug2 = generate_project_slug(title, project_id)
    assert slug1 == slug2


def test_generate_project_slug_with_non_string_id():
    """
    Test that generate_project_slug handles non-string project_id.
    """
    project_id = 123456789
    title = "Non-string ID"
    short_id = str(project_id)[:8]
    expected_slug = f"non-string-id-{short_id}"
    slug = generate_project_slug(title, project_id)
    assert slug == expected_slug
