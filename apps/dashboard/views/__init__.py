from .home import HomeView
from .accounts.login import LoginView
from .accounts.logout import LogoutView
from .accounts.forgot_password import ForgotPasswordView
from .accounts.forgot_password_verify import ForgotPasswordVerifyView
from .customers import CustomerListView, CustomerDetailView
from .cooks import CookListView, CookDetailView
from .couriers import CourierListView, CourierDetailView
from .orders import OrderListView, OrderDetailsView, OrderView
from .rating import RatingListView
from .contents import (
    StaticContentView,
    TermAndConditionDetailView,
    TermAndConditionUpdateView,
    PrivacyPolicyDetailView,
    PrivacyPolicyUpdateView,
    BannerListView,
    BannerCreateView
)