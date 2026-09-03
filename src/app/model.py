from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserState(Base):
    __tablename__ = "UserState"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    state: Mapped[str] = mapped_column()
