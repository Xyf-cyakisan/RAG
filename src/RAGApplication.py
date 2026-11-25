from pathlib import Path
from .Answerer import Answerer
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
        dataset_path: str = Path("data/datasets/UnansweredQuestions/"
                                 "dataset_docs_public.json"),
        k: int = 5,
        save_directory: str = Path("data/output/search_results"
                                   "/UnansweredQuestions"),
    ) -> None:
        dataset_path = (Path(dataset_path) if
                        isinstance(dataset_path, str) else dataset_path)
        save_directory = (Path(save_directory) if
                          isinstance(save_directory, str) else save_directory)
        chunks = JsonManager.get_indices()
        JsonManager.write_in_json(
            save_directory.as_posix() + "/" + dataset_path.name,
            Researcher.research_best_chunk(chunks, k, dataset_path),
        )

    @staticmethod
    def answer(query: str, k: int = 5) -> str:
        if query == "":
            raise ValueError("Query must be a defined non empty string.")
        retriever = bm25s.BM25()
        chunks = JsonManager.get_indices()
        token_chunks = [
            Researcher.tokenizer_code_avancé(text)
            for text in Researcher.get_txt_chunks(chunks)
        ]
        retriever.index(token_chunks)
        best_chunks = Researcher.search(
            query,
            retriever,
            chunks,
            k
        )
        text_sources = []
        for source in best_chunks:
            text_sources.append(Path(source.file_path).read_text(
            )[source.first_character_index: source.last_character_index + 1])
        tokenizer, llm = Answerer.get_tokenizer_and_llm()
        answer = Answerer.get_answer(query, best_chunks,
                                     text_sources, tokenizer, llm)
        JsonManager.write_in_json(
            "data/output/search_results_and_answers/single_query.json",
            answer)
        return answer.answer

    @staticmethod
    def answer_dataset(
        student_search_results_path: Path = Path("data/output/search_results/"
                                                 "UnansweredQuestions/"
                                                 "dataset_docs_public.json"),
        save_directory: Path = Path("data/output/search_results_and_answer")
    ) -> None:
        student_search_results_path = (Path(student_search_results_path) if
                                       isinstance(
                                           student_search_results_path, str)
                                       else student_search_results_path)
        save_directory = (Path(save_directory) if
                          isinstance(save_directory, str) else save_directory)
        retriever = bm25s.BM25()
        chunks = JsonManager.get_indices()
        token_chunks = [
            Researcher.tokenizer_code_avancé(text)
            for text in Researcher.get_txt_chunks(chunks)
        ]
        retriever.index(token_chunks)
        JsonManager.write_in_json(
            save_directory.as_posix() + "/" + student_search_results_path.name,
            Answerer.get_answer_dataset(student_search_results_path,
                                        retriever, chunks)
            )

    @staticmethod
    def evaluate(
        student_search_results_path: Path, dataset_path: Path
    ) -> None:
        ...
