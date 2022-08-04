from .dashboard import DashboardView
from .survey import SurveyDateView
from .qrcode_form import QRCodeFormView, SurveyStoppedView, SurveyPusedView, EndSurveyView, SurveyStartView
from .login import LoInFunc

__all__ = [
    DashboardView,
    SurveyDateView,
    QRCodeFormView,
    SurveyStoppedView,
    SurveyPusedView,
    EndSurveyView,
    SurveyStartView,
    LoInFunc,
]
