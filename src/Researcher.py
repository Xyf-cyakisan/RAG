from .data_models import MinimalSearchResults, MinimalSource, RagDataset, StudentSearchResults
import bm25s
import re
from pathlib import Path
from tqdm import tqdm


class Researcher:

    KEYWORDS_PYTHON: set[str] = {
        "def", "class", "import", "from", "return",
        "if", "else", "elif", "for", "while",
        "try", "except", "with", "as", "pass",
        "none", "true", "false", "and", "or", "not",
        "in", "is", "lambda", "yield", "async",
        "await", "self",
    }

    @staticmethod
    def get_txt_chunks(og_chunks: list[MinimalSource]) -> list[str]:
        text_chunks = []
        for chunk in og_chunks:
            with open(chunk["file_path"], "r") as file:
                text_chunks.append(file.read()[
                    chunk["first_character_index"]:
                    chunk["last_character_index"]])
        return text_chunks

    @staticmethod
    def tokenizer_code_avancé(
        texte: str,
        exclure_keywords: set = KEYWORDS_PYTHON,
        min_len: int = 3
    ) -> list[str]:
        """
        Tokenizer code avancé avec exclusion des mots-clés du langage.
        Idéal quand on indexe des fonctions Python / JS.
        """
        # Séparer camelCase / PascalCase
        texte = re.sub(r'([a-z])([A-Z])', r'\1 \2', texte)
        texte = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', texte)

        # Remplacer les séparateurs
        texte = re.sub(r'[_\-./\\:@#()\[\]{}<>,;=!?|&*+%^~`"\']+', ' ', texte)

        # Tokeniser
        tokens = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', texte)
        tokens = [t.lower() for t in tokens]

        # Filtrer
        return [
            t for t in tokens
            if len(t) >= min_len and t not in exclure_keywords
        ]

    @staticmethod
    def research_best_chunk(chunks: list[MinimalSource], k: int,
                            dataset_path: Path
                            ) -> list[MinimalSearchResults]:
        text_chunks = Researcher.get_txt_chunks(chunks)
        token_chunks = [Researcher.tokenizer_code_avancé(text)
                        for text in text_chunks]
        retriever = bm25s.BM25()
        retriever.index(token_chunks)
        return Researcher.search_dataset(
                dataset_path=dataset_path,
                retriever=retriever,
                all_chunks=chunks,
                k=k
            )

    @staticmethod
    def search(
        query: str,
        retriever: bm25s.BM25,
        all_chunks: list[MinimalSource],
        k: int = 5,
    ) -> list[MinimalSource]:
        query_tokens = [Researcher.tokenizer_code_avancé(query)]

        indices, _ = retriever.retrieve(
            query_tokens,
            k=min(k, len(all_chunks)),
        )

        sources = []
        for chunk_index in indices[0]:
            source = all_chunks[int(chunk_index)]
            sources.append(source)

        return sources

    @staticmethod
    def search_dataset(
        dataset_path: str,
        retriever: bm25s.BM25,
        all_chunks: list[tuple[str, MinimalSource]],
        k: int = 10,
    ) -> None:
        # Lire les questions et les convertir en objets Pydantic.
        dataset_file = Path(dataset_path)
        dataset = RagDataset.model_validate_json(
            dataset_file.read_text(encoding="utf-8")
        )

        results = []

        for question in tqdm(
            dataset.rag_questions,
            desc="Recherche des sources",
            unit="question",
        ):
            sources = Researcher.search(
                query=question.question,
                retriever=retriever,
                all_chunks=all_chunks,
                k=k,
            )

            results.append(
                MinimalSearchResults(
                    question_id=question.question_id,
                    question=question.question,
                    retrieved_sources=sources,
                )
            )

        # Regrouper tous les résultats dans le format attendu.
        output = StudentSearchResults(
            search_results=results,
            k=k,
        )
        return output
