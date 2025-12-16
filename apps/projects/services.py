from django.utils.text import slugify

def generate_project_slug(title: str, project_id: str) -> str:
    """
    Generate a unique slug for a project based on its title and ID.

    Args:
        title (str): The title of the project.
        project_id (str): The unique identifier of the project.

    Returns:
        str: A unique slug for the project.
    """
    base_slug = slugify(title)
    short_id = str(project_id)[:8]

    unique_slug = f"{base_slug}-{short_id}"
    return unique_slug