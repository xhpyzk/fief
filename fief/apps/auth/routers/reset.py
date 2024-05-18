from fastapi import APIRouter, Depends, Header, Query, Request, status
from fastapi.responses import RedirectResponse

from fief.apps.auth.forms.reset import ForgotPasswordForm, ResetPasswordForm
from fief.dependencies.auth import (
    BaseContext,
    get_base_context,
    get_optional_login_session,
)
from fief.dependencies.tenant import get_current_tenant
from fief.dependencies.users import get_user_manager
from fief.forms import FormHelper
from fief.locale import gettext_lazy as _
from fief.models import LoginSession, Tenant
from fief.services.user_manager import (
    InvalidResetPasswordTokenError,
    UserDoesNotExistError,
    UserInactiveError,
    UserManager,
)

router = APIRouter()


@router.api_route("/forgot", methods=["GET", "POST"], name="reset:forgot")
async def forgot_password(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
    tenant: Tenant = Depends(get_current_tenant),
    context: BaseContext = Depends(get_base_context),
):
    form_helper = FormHelper(
        ForgotPasswordForm,
        "auth/forgot_password.html",
        request=request,
        context={**context},
    )
    form = await form_helper.get_form()

    if await form_helper.is_submitted_and_valid():
        try:
            user = await user_manager.get_by_email(form.email.data, tenant.id)
            await user_manager.forgot_password(user, request=request)
        except (UserDoesNotExistError, UserInactiveError):
            pass

        form_helper.context["success"] = _(
            "Check your inbox! If an account associated with this email address exists in our system, you'll receive a link to reset your password."
        )

    return await form_helper.get_response()


@router.api_route("/reset", methods=["GET", "POST"], name="reset:reset")
async def reset_password(
    request: Request,
    hx_trigger: str | None = Header(None),
    token: str | None = Query(None),
    user_manager: UserManager = Depends(get_user_manager),
    login_session: LoginSession | None = Depends(get_optional_login_session),
    tenant: Tenant = Depends(get_current_tenant),
    context: BaseContext = Depends(get_base_context),
):
    form_helper = FormHelper(
        ResetPasswordForm,
        "auth/reset_password.html",
        request=request,
        context={**context},
    )
    form = await form_helper.get_form()

    if request.method == "GET":
        if token is None:
            return await form_helper.get_error_response(
                _("The reset password token is missing."), "missing_token", fatal=True
            )
        else:
            form.token.data = token

    if await form_helper.is_submitted_and_valid() and hx_trigger is None:
        try:
            await user_manager.reset_password(
                form.token.data, form.password.data, tenant, request=request
            )
        except (
            InvalidResetPasswordTokenError,
            UserDoesNotExistError,
            UserInactiveError,
        ):
            return await form_helper.get_error_response(
                _("The reset password token is invalid or expired."),
                "invalid_token",
                fatal=True,
            )
        else:
            # if login_session is not None:
            redirection = tenant.url_path_for(request, "auth:login")
            return RedirectResponse(
                url=redirection, status_code=status.HTTP_302_FOUND
            )

    return await form_helper.get_response()
