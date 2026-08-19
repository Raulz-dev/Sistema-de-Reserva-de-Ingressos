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
        self.title = self._validate_title(self.title)
        self.synopsis = self._validate_synopsis(self.synopsis)
        self.age_rating = self._validate_age_rating(self.age_rating)
        self.duration_minutes = self._validate_duration_minutes(
            self.duration_minutes
        )
        self.genre = self._validate_genre(self.genre)
        self.trailer_url = self._validate_trailer_url(self.trailer_url)

    def change_title(self, new_title: str) -> None:
        self.title = self._validate_title(new_title)

    def change_synopsis(self, new_synopsis: str) -> None:
        self.synopsis = self._validate_synopsis(new_synopsis)

    def change_age_rating(self, new_age_rating: str) -> None:
        self.age_rating = self._validate_age_rating(new_age_rating)

    def change_duration_minutes(self, new_duration_minutes: int) -> None:
        self.duration_minutes = self._validate_duration_minutes(new_duration_minutes)

    def change_genre(self, new_genre: str) -> None:
        self.genre = self._validate_genre(new_genre)

    def change_trailer_url(self, new_trailer_url: str | None) -> None:
        self.trailer_url = self._validate_trailer_url(new_trailer_url)

    @classmethod
    def _validate_title(cls, title: str) -> str:
        return cls._required_text(title, "título")

    @classmethod
    def _validate_synopsis(cls, synopsis: str) -> str:
        return cls._required_text(synopsis, "sinopse")

    @classmethod
    def _validate_age_rating(cls, age_rating: str) -> str:
        return cls._required_text(age_rating, "classificação indicativa")

    @staticmethod
    def _validate_duration_minutes(duration_minutes: int) -> int:
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise InvalidMovieError("A duração deve ser um número inteiro positivo.")
        return duration_minutes

    @classmethod
    def _validate_genre(cls, genre: str) -> str:
        return cls._required_text(genre, "gênero")

    @staticmethod
    def _validate_trailer_url(trailer_url: str | None) -> str | None:
        return trailer_url

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidMovieError(f"O campo {field_name} é obrigatório.")
        return value.strip()
