from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    organization: str
    url: str
    published: str
    license: str
    reuse_authorized: bool
    file: str
    sha256: str
    pages: list[int] | None = None


@dataclass(frozen=True)
class Page:
    source: Source
    number: int  # posición física en PDF, base 1
    label: str
    text: str


@dataclass(frozen=True)
class Chunk:
    id: str
    source_id: str
    title: str
    url: str
    license: str
    document_sha256: str
    page: int
    page_label: str
    start_word: int
    text: str

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float

