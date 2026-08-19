from dataclasses import dataclass, field
from uuid import UUID, uuid7

from app.movies.domain.exceptions import InvalidMovieError


@dataclass(slots=True)
class Movie:
    title: str
    synopsis: str
    age_rating: str
    duration_minutes: int
    genre: str
    trailer_url: str | None = None
    id: UUID = field(default_factory=uuid7)

    def __post_init__(self) -> None:
        self.title = self._required_text(self.title, "título")
        self.synopsis = self._required_text(self.synopsis, "sinopse")
        self.age_rating = self._required_text(
            self.age_rating, "classificação indicativa"
        )
        self.genre = self._required_text(self.genre, "gênero")

        if not isinstance(self.duration_minutes, int) or self.duration_minutes <= 0:
            raise InvalidMovieError("A duração deve ser um número inteiro positivo.")

    def change_title(self, new_title: str) -> None:
        self.title = self._required_text(new_title, "título")

    def change_synopsis(self, new_synopsis: str) -> None:
        self.synopsis = self._required_text(new_synopsis, "sinopse")

    def change_age_rating(self, new_age_rating: str) -> None:
        self.age_rating = self._required_text(
            new_age_rating, "classificação indicativa"
        )

    def change_duration_minutes(self, new_duration_minutes: int) -> None:
        if not isinstance(new_duration_minutes, int) or new_duration_minutes <= 0:
            raise InvalidMovieError("A duração deve ser um número inteiro positivo.")
        self.duration_minutes = new_duration_minutes

    def change_genre(self, new_genre: str) -> None:
        self.genre = self._required_text(new_genre, "gênero")

    def change_trailer_url(self, new_trailer_url: str | None) -> None:
        self.trailer_url = new_trailer_url

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidMovieError(f"O campo {field_name} é obrigatório.")
        return value.strip()
