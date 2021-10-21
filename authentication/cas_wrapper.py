from django_cas_ng import views as cas_views
from django_cas_ng.models import ProxyGrantingTicket, SessionTicket
from django_cas_ng.utils import get_protocol, get_redirect_url, get_cas_client
from django_cas_ng.signals import cas_user_logout
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from urllib import parse as urllib_parse
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from .models import User

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class APILoginView(cas_views.LoginView):

    def successful_login(self, request: HttpRequest, next_page: str) -> HttpResponse:
        """
        This method is called on successful login. Override this method for
        custom post-auth actions (i.e, to add a cookie with a token).

        :param request:
        :param next_page:
        :return:
        """
        try:
            user = User.objects.get(email=f'{request.user.email}@ui.ac.id')
        except User.DoesNotExist:
            user = request.user

        new_next_page = next_page

        if user.email == "":
            new_next_page = settings.SUCCESS_SSO_AUTH_REDIRECT + 'not-login/'
            user.delete()
        elif not user.is_active:
            new_next_page = settings.SUCCESS_SSO_AUTH_REDIRECT + 'not-login/'
        else:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

            new_next_page = settings.SUCCESS_SSO_AUTH_REDIRECT + 'login-sivitas/' + jwt_token

        return HttpResponseRedirect(new_next_page)


class APILogoutView(cas_views.LogoutView):

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Redirects to CAS logout page

        :param request:
        :return:
        """
        next_page = settings.SUCCESS_SSO_AUTH_REDIRECT

        # try to find the ticket matching current session for logout signal
        try:
            st = SessionTicket.objects.get(session_key=request.session.session_key)
            ticket = st.ticket
        except SessionTicket.DoesNotExist:
            ticket = None
        # send logout signal
        cas_user_logout.send(
            sender="manual",
            user=request.user,
            session=request.session,
            ticket=ticket,
        )

        # clean current session ProxyGrantingTicket and SessionTicket
        ProxyGrantingTicket.objects.filter(session_key=request.session.session_key).delete()
        SessionTicket.objects.filter(session_key=request.session.session_key).delete()
        auth_logout(request)

        next_page = next_page or get_redirect_url(request)
        if settings.CAS_LOGOUT_COMPLETELY:
            client = get_cas_client(request=request)
            return HttpResponseRedirect(client.get_logout_url(next_page))

        # This is in most cases pointless if not CAS_RENEW is set. The user will
        # simply be logged in again on next request requiring authorization.
        return HttpResponseRedirect(next_page)
