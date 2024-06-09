def save_github_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        avatar_url = response.get('avatar_url')
        if avatar_url:
            profile = user.profile
            profile.avatar_url = avatar_url
            profile.save()
