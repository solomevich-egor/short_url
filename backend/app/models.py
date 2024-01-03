from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


metadata = Base.metadata


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    target_url: Mapped[str] = mapped_column(index=True, unique=True)
    key: Mapped[str] = mapped_column(index=True, unique=True)
    secret_key: Mapped[str] = mapped_column(index=True, unique=True)