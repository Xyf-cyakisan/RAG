from pathlib import Path
from pydantic import BaseModel
import json
from .data_models import MinimalSource


class JsonManager:
    @staticmethod
    def write_in_json(file_name: str, datas: list[BaseModel] | BaseModel
                      ) -> None:
        print(file_name)
        file = Path(file_name)
        file.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(datas, list):
            to_dump = [data.model_dump(mode="json") for
                       data in datas]
        else:
            to_dump = datas.model_dump(mode="json")
        with open(file, "w") as output_file:
            json.dump(to_dump, output_file, indent=4)

    @staticmethod
    def get_indices() -> list[MinimalSource]:
        try:
            with open(
                "data/processed/indices.json", encoding="utf-8"
            ) as indice_file:
                chunks: list[MinimalSource] = json.load(indice_file)
                return chunks
        except FileNotFoundError:
            raise FileNotFoundError("Warning, 'data/processed/indices.json'"
                                    " file not found, please run 'make index' "
                                    "or 'python3 -m index' commands first.")
