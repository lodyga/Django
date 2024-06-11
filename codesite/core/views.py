from django.shortcuts import render


def index_view(request):
    social_auth = request.user.social_auth.last()
    print(social_auth.provider)
    print("ala")
    print(request.user.social_auth.get(provider="github"))
    print("ala")
    print(request.user.social_auth.model)
    print("ala")
    print(request.user.social_auth.all())
    print("ala")
    print(request.user.social_auth.values())
    # print(request.user.social_auth.get('provider'))
    return render(request, "core/index.html")


def contact_view(request):
    return render(request, "core/contact.html")

