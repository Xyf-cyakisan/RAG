from pathlib import Path
from .data_models import MinimalSearchResults
from .Researcher import Researcher
from .Chunker import Chunker
from .JsonManager import JsonManager
import bm25s


class RAGApplication:
    @staticmethod
    def index(max_chunk_size: int = 2000) -> None:
        JsonManager.write_in_json(
            "data/processed/indices.json", Chunker.get_chunks(max_chunk_size)
        )

    @staticmethod
    def search(query: str, k: int = 5) -> None:
        if query == "":
            raise ValueError("Query must be a defined non empty string.")
        retriever = bm25s.BM25()
        chunks = JsonManager.get_indices()
        token_chunks = [
            Researcher.tokenizer_code_avancé(text)
            for text in Researcher.get_txt_chunks(chunks)
        ]
        retriever.index(token_chunks)
        JsonManager.write_in_json(
            Path(
                "data/output/search_results"
                "/UnansweredQuestions/single_query.json"
            ),
            MinimalSearchResults(
                question_id="\\",
                question=query,
                retrieved_sources=Researcher.search(
                    query, retriever, chunks, k
                ),
            ),
        )

    @staticmethod
    def search_dataset(
        dataset_path: str = "data/datasets/UnansweredQuestions/"
        "dataset_docs_public.json",
        k: int = 5,
        save_directory: str = "data/output/search_results"
        "/UnansweredQuestions",
    ) -> None:
        dataset_path = Path(dataset_path)
        save_directory = Path(save_directory)
        chunks = JsonManager.get_indices()
        JsonManager.write_in_json(
            save_directory.as_posix() + "/" + dataset_path.name,
            Researcher.research_best_chunk(chunks, k, dataset_path),
        )

    @staticmethod
    def answer(k: int = 5) -> None:
        ...

    @staticmethod
    def answer_dataset(
        student_search_results_path: Path, save_directory: Path
    ) -> None:
        ...

    @staticmethod
    def evaluate(
        student_search_results_path: Path, dataset_path: Path
    ) -> None:
        ...
