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
    db.query(OnboardingResponse).filter(
        OnboardingResponse.user_id == current_user.id
    ).delete()
    for answer in data.response:
        db.add(
            OnboardingResponse(
                user_id=current_user.id,
                question_key=answer.question_key,
                answer_value=answer.answer_value,
            )
        )

    response_map = {a.question_key: a.answer_value for a in data.response}

    existing_persona = db.get(UserPersona, current_user.id)
    persona = get_persona_from_responses(response_map, existing_persona)
    persona.user_id = current_user.id
    if existing_persona is None:
        db.add(persona)

    profile = db.get(UserProfile, current_user.id)
    if profile is None:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    profile.onboarding_completed = True

    db.commit()
    db.refresh(persona)

    return OnboardingSummaryResponse(
        persona=PersonaResponse.model_validate(persona),
        recommended_plan=RecommendedPlanResponse(**build_recommended_plan(persona)),
    )


@router.get("/summary", response_model=OnboardingSummaryResponse)
def onboarding_summary(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    persona = db.get(UserPersona, current_user.id)
    if persona is None:
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
