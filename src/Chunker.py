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
        for path in tqdm.tqdm([path for path in Path("data/raw").rglob("*") if
                               path.name.endswith((".py", ".md", ".txt"))],
                              desc="Chunking all data files", unit="file"):
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
        chunks = []
        text = file.read_text()
        len_text = len(text)
        start = 0
        while True:
            if start + max_chunk_size - 1 >= len_text:
                end = len_text - 1
            elif text[start:start + max_chunk_size].rfind(".") != -1:
                end = start + text[start:start + max_chunk_size].rfind(".")
            else:
                end = start + max_chunk_size - 1
            chunks.append(
                MinimalSource(file_path=file.as_posix(),
                              first_character_index=start,
                              last_character_index=end)
            )
            if end == len_text - 1:
                break
            start += max_chunk_size
            start = start - (max_chunk_size // 40)
        return chunks

    @staticmethod
    def __cut_python_file(file: Path, max_chunk_size: int
                          ) -> list[MinimalSource]:
        source = file.read_text()
        tree = ast.parse(source, filename=str(file))

        chunks: list[MinimalSource] = []
        length = [0]
        for line in source.splitlines(keepends=True):
            length.append(length[-1] + len(line))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef,
                                 ast.AsyncFunctionDef)):
                first_line = node.lineno
                if node.decorator_list:
                    first_line = node.decorator_list[0].lineno
                end_line = node.end_lineno
                start = length[first_line - 1]
                end = length[end_line]
                for chunk_s in range(start, end, max_chunk_size):
                    if (chunk_s + max_chunk_size - 1) >= end:
                        chunk_e = end
                    else:
                        chunk_e = chunk_s + max_chunk_size
                    chunks.append(MinimalSource(
                        file_path=file.as_posix(),
                        first_character_index=chunk_s,
                        last_character_index=chunk_e)
                                                )
        return chunks
