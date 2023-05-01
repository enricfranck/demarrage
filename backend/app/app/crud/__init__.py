
from .crud_user import user
from .crud_role import role
from .crud_company import company
from .crud_team import team
from .crud_site import site
from .crud_inspection_condition import inspection_condition
from .crud_inspection_type import inspection_type
from .crud_category import category
from .crud_status import status
from .crud_risk import risk
from .crud_assessment import assessment
from .crud_calibration import calibration
from .crud_record import record
from .crud_equipment_group import equipment_group
from .crud_recomendation_status import recommendation_status
from .crud_failure_progress import failure_progress
from .crud_defect import defect
from .crud_plant import plant
from .crud_criticality import criticality
from .crud_equipment import equipment
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
