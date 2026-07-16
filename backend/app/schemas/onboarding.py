from typing import Literal, Optional

from pydantic import BaseModel, Field

QuestionType = Literal["single_choice"]


class OnboardingQuestionOption(BaseModel):
    label: str
    value: str


class OnboardingQuestion(BaseModel):
    key: str
    title: str
    description: Optional[str] = None
    type: QuestionType = "single_choice"
    options: list[OnboardingQuestionOption]


class OnboardingQuestionResponse(BaseModel):
    questions: list[OnboardingQuestion]


class OnboardingAnswer(BaseModel):
    question_key: str = Field(min_length=1, max_length=100)
    answer_value: str = Field(min_length=1, max_length=255)


class OnboardingComplete(BaseModel):
    response: list[OnboardingAnswer] = Field(min_length=1)


class PersonaResponse(BaseModel):
    primary_goal: Optional[str] = None
    main_challenge: Optional[str] = None
    income_type: Optional[str] = None
    pay_frequency: Optional[str] = None
    confidence_level: Optional[str] = None
    behaviour_pattern: Optional[str] = None
    spending_trigger: Optional[str] = None
    coaching_style: Optional[str] = None
    setup_preferences: Optional[str] = None
    thirty_day_win: Optional[str] = None

    model_config = {"from_attributes": True}


class RecommendedPlanResponse(BaseModel):
    budget_type: str
    first_lesson_slug: str
    first_challenge_slug: str
    home_focus: str


class OnboardingSummaryResponse(BaseModel):
    persona: PersonaResponse
    recommended_plan: RecommendedPlanResponse
