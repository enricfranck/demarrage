from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, roles, company, team, site, category,\
    inspection_type, inspection_condition, status, risk, assessment, calibration, equipment_group,\
    recommendation_status, failure_progress, defect, plant, criticality, equipment


api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(company.router, prefix="/company", tags=["Company"])
api_router.include_router(team.router, prefix="/team", tags=["Team"])
api_router.include_router(site.router, prefix="/site", tags=["Site"])
api_router.include_router(category.router, prefix="/category", tags=["Category"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(risk.router, prefix="/risk", tags=["Risk"])
api_router.include_router(inspection_condition.router, prefix="/inspection_condition", tags=["Inspection Condition"])
api_router.include_router(inspection_type.router, prefix="/inspection_type", tags=["Inspection Type"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
api_router.include_router(calibration.router, prefix="/calibration", tags=["Calibration"])
api_router.include_router(equipment_group.router, prefix="/equipment_group", tags=["Equipment Group"])
api_router.include_router(recommendation_status.router, prefix="/recommendation_status", tags=["Recommendation Status"])
api_router.include_router(failure_progress.router, prefix="/failure_progress", tags=["Failure Progress"])
api_router.include_router(defect.router, prefix="/defect", tags=["defect"])
api_router.include_router(plant.router, prefix="/plant", tags=["plant"])
api_router.include_router(criticality.router, prefix="/criticality", tags=["criticality"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
