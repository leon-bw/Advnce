from app.models.onboarding import UserPersona


def get_persona_from_responses(
    response_map: dict[str, str], existing_persona: UserPersona | None = None
) -> UserPersona:

    if existing_persona:
        persona = existing_persona
    else:
        persona = UserPersona(user_id=response_map.get("user_id"))

    Persona_Response_Fields = [
        "primary_goal",
        "main_challenge",
        "income_type",
        "pay_frequency",
        "confidence_level",
        "behaviour_pattern",
        "spending_trigger",
        "coaching_style",
        "setup_preferences",
        "thirty_day_win",
    ]

    for response_fields in Persona_Response_Fields:
        setattr(persona, response_fields, response_map.get(response_fields))

    return persona


def build_recommended_plan(persona: UserPersona) -> dict:
    budget_type = "monthly"
    if persona.pay_frequency in {"weekly", "fortnightly"}:
        budget_type = "weekly"
    if persona.income_type in {"variable_income", "self_employed", "mixed_income"}:
        budget_type = "custom"

    home_focus = "spending_control"
    if persona.primary_goal == "build_savings":
        home_focus = "savings_growth"
    elif persona.primary_goal == "pay_off_debt":
        home_focus = "debt_reduction"
    elif persona.primary_goal == "reduce_money_stress":
        home_focus = "confidence_building"

    first_lesson_slug = "budget-basics"
    if persona.confidence_level in {"confident", "very_confident"}:
        first_lesson_slug = "cash-flow-planning"
    if persona.spending_trigger == "stressed":
        first_lesson_slug = "spending-triggers-101"

    first_challenge_slug = "track-every-purchase-today"
    if persona.primary_goal == "build_savings":
        first_challenge_slug = "save-your-first-10"
    elif persona.primary_goal == "pay_off_debt":
        first_challenge_slug = "review-one-debt-payment"
    elif persona.primary_goal == "reduce_money_stress":
        first_challenge_slug = "do-a-2-minute-money-checkin"

    return {
        "budget_type": budget_type,
        "first_lesson_slug": first_lesson_slug,
        "first_challenge_slug": first_challenge_slug,
        "home_focus": home_focus,
    }
