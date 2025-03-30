from dataclasses import dataclass, asdict

@dataclass
class Movie:
    title: str
    rating: float
    num_reviews: int
    num_oscars: int
    adjusted_rating: float = None

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Movie(
            title=data['title'],
            rating=data['rating'],
            num_reviews=data['num_reviews'],
            num_oscars=data['num_oscars'],
            adjusted_rating=data.get('adjusted_rating')
        )
