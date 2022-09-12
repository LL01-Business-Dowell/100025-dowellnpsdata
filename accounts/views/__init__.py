from .dashboard import DashboardView
from .survey import SurveyDateView, MySurveysView
from .qrcode_form import QRCodeFormView, SurveyStoppedView, SurveyPusedView, EndSurveyView, SurveyStartView
from .login import LoInFunc

__all__ = [
    DashboardView,
    SurveyDateView,
    MySurveysView,
    QRCodeFormView,
    SurveyStoppedView,
    SurveyPusedView,
    EndSurveyView,
    SurveyStartView,
    LoInFunc,
]
