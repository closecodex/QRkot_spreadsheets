from sqlalchemy import Column, Integer, String

from .base import InvestmentBaseModel

NAME_MAX_LENGTH = 100
DEFAULT_INVESTED_AMOUNT = 0


class CharityProject(InvestmentBaseModel):

    name = Column(
        String(NAME_MAX_LENGTH), unique=True, index=True, nullable=False
    )
    description = Column(String, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)

    def __repr__(self):
        """Отладочное представление модели CharityProject."""
        base_repr = super().__repr__()
        return (
            f'{base_repr[:-1]}, name={self.name}, '
            f'description={self.description})'
        )
