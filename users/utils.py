def user_directory_path(instance, filename):
    """
    Returns the path to the user's profile photo directory.
    The path is structured as 'user_<user_id>/<filename>'.
    """
    return f'user_{0}/{1}'.format(instance.user.id, filename)