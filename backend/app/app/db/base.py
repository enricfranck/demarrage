# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.company import Company  # noqa
from app.models.site import Site  # noqa
from app.models.team import Team  # noqa
from app.models.user import User  # noqa
from app.models.role import Role # noqa
from app.models.inspection_type import InspectionType # noqa
from app.models.inspection_condition import InspectionCondition # noqa
from app.models.status import Status # noqa
from app.models.category import Category # noqa
from app.models.risk import Risk # noqa
from app.models.assessment import Assessment # noqa
from app.models.defect import Defect # noqa
from app.models.equipment_group import EquipmentGroup # noqa
from app.models.record import Record # noqa
from app.models.failure_progress import FailureProgress # noqa
from app.models.recommendation_status import RecommendationStatus # noqa
from app.models.calibration import Calibration # noqa
from app.models.equipment import Equipment # noqa
