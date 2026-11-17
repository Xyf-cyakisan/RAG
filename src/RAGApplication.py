from pathlib import Path
from .Chunker import Chunker


class RAGApplication:
    @staticmethod
    def index(max_chunk_size: int = 2000) -> None:
        print(len(Chunker.get_chunks(max_chunk_size)))

    @staticmethod
    def search_dataset(dataset_path: Path, k: int,
                       save_directory: Path) -> None:
        ...

    @staticmethod
    def answer_dataset(student_search_results_path: Path,
                       save_directory: Path) -> None:
        ...
