"""A simple user management API module."""

def get_user(user_id: int) -> dict:
    """
    Retrieves a user profile by their unique ID.

    This endpoint queries the primary user database.

    :param user_id: The unique identifier of the user to retrieve.
    :type user_id: int
    :raises ValueError: If the user ID is negative.
    :return: A dictionary containing the user's profile data.
    :rtype: dict
    """
    pass

def create_post(title: str, body: str, author_id: int) -> dict:
    """
    Creates a new blog post associated with a specific author.

    :param title: The title of the new post.
    :type title: str
    :param body: The full content of the post.
    :type body: str
    :param author_id: The ID of the user creating the post.
    :type author_id: int
    :return: The newly created post object with its generated ID.
    :rtype: dict
    """
    pass