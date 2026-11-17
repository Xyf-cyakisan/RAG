import ast
from pathlib import Path
from typing import Callable
from .data_models import MinimalSource
import tqdm


class Chunker:
    @staticmethod
    def __get_file_cutter(file_type: str) -> Callable:
        return {
            "TEXT": Chunker.__cut_file,
            "MARKDOWN": Chunker.__cut_file,
            "PYTHON": Chunker.__cut_python_file
        }[file_type]

    @staticmethod
    def get_chunks(max_chunk_size: int) -> list[MinimalSource]:
        chunks: list[MinimalSource] = []
        for path in tqdm.tqdm([path for path in Path("data/raw").rglob("*") if path.name.endswith((".py", ".md", ".txt"))], desc="Gautier est trop beau", unit="file"):
            chunks.extend(Chunker.__get_file_cutter(
                Chunker.__get_file_type(path))(
                    path, max_chunk_size))
        return chunks

    @staticmethod
    def __get_file_type(file: Path) -> str:
        if file.name.endswith(".py"):
            return "PYTHON"
        elif file.name.endswith(".md"):
            return "MARKDOWN"
        else:
            return "TEXT"

    @staticmethod
    def __cut_file(file: Path, max_chunk_size: int) -> list[MinimalSource]:
        cut = []
        start = 0
        end = 0
        file_end = len(file.read_text())
        while end != file_end:
            end += max_chunk_size
            if end > file_end:
                end = file_end
            cut.append(MinimalSource(file_path=file.as_posix(),
                                     first_character_index=start,
                                     last_character_index=end))
            start = end
        return cut

    @staticmethod
    def __cut_python_file(file: Path, max_chunk_size: int
                          ) -> list[MinimalSource]:
        source = file.read_text()
        tree = ast.parse(source, filename=str(file))

        chunks: list[str] = []
        length = [len(line) for line in source.splitlines(True)]
        length = [0] + length
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                chunk = ast.get_source_segment(source, node)
                if chunk:
                    if len(chunk) > max_chunk_size:
                        start = 0
                        end = 0
                        file_end = len(chunk)
                        while end != file_end:
                            end += max_chunk_size
                            if end > file_end:
                                end = file_end
                            chunks.append(MinimalSource(file_path=file.as_posix(),
                                                        first_character_index=start,
                                                        last_character_index=end))
                            start = end
                    else:
                        chunks.append(MinimalSource(
                            file_path=file.as_posix(),
                            first_character_index=length[node.lineno - 1] + 1,
                            last_character_index=length[node.end_lineno - 1] + 1
                        ))
        return chunks
