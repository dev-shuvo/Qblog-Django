def detectUser(user):
    if user.user_type == "author":
        redirectUrl = "/author-dashboard/"
        return redirectUrl
    elif user.user_type == "normal":
        redirectUrl = "/user-dashboard/"
        return redirectUrl
    elif user.user_type == None and user.is_superAdmin:
        redirectUrl = "/admin"
        return redirectUrl
