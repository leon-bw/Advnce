import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(120), nullable=True)
    currency_code: Mapped[str] = mapped_column(String(3), default="GBP", nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), default="GB", nullable=False)
    timezone: Mapped[str] = mapped_column(
        String(64), default="Europe/London", nullable=False
    )
    theme: Mapped[str] = mapped_column(String(255), default="system", nullable=False)
    onboarding_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")


class OnboardingResponse(Base):
    __tablename__ = "onboarding_responses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    answer_value: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="onboarding_responses")


class UserPersona(Base):
    __tablename__ = "user_personas"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    primary_goal: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    main_challenge: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    income_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pay_frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    confidence_level: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    behaviour_pattern: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    spending_trigger: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    coaching_style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    setup_preferences: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    thirty_day_win: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="persona")
