from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.onboarding import OnboardingResponse, UserPersona, UserProfile
from app.models.user import User
from app.schemas.onboarding import (
    OnboardingComplete,
    OnboardingSummaryResponse,
    PersonaResponse,
    RecommendedPlanResponse,
)
from backend.app.services.onboarding_service import (
    build_recommended_plan,
    get_persona_from_responses,
)

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("/complete", response_model=OnboardingSummaryResponse)
def complete_onboarding(
    data: OnboardingComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not data.response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Responses are required"
        )

    profile = (
        db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    )
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    db.query(OnboardingResponse).filter(
        OnboardingResponse.user_id == current_user.id
    ).delete()

    response_map = {"user_id": current_user.id}
    for item in data.response:
        db.add(
            OnboardingResponse(
                user_id=current_user.id,
                question_key=item.question_key,
                answer_value=item.answer_value,
            )
        )
        response_map[item.question_key] = item.answer_value

    existing_persona = (
        db.query(UserPersona).filter(UserPersona.user_id == current_user.id).first()
    )
    persona = get_persona_from_responses(response_map, existing_persona)

    if existing_persona is None:
        db.add(persona)

    profile.onboarding_completed = True

    db.commit()
    db.refresh(persona)

    return OnboardingSummaryResponse(
        persona=PersonaResponse.model_validate(persona),
        recommended_plan=RecommendedPlanResponse(**build_recommended_plan(persona)),
    )


@router.get("/summary", response_model=OnboardingSummaryResponse)
def get_onboarding_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    persona = (
        db.query(UserPersona).filter(UserPersona.user_id == current_user.id).first()
    )
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Onboarding not complete"
        )

    return OnboardingSummaryResponse(
        persona=PersonaResponse.model_validate(persona),
        recommended_plan=RecommendedPlanResponse(**build_recommended_plan(persona)),
    )


@router.get("/status")
def onboarding_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.get(UserProfile, current_user.id)
    return {"completed": bool(profile and profile.onboarding_completed)}
