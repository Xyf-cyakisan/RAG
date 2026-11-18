.SILENT: install index search search_dataset

MAX_CHUNK_SIZE = 2000
K = 5
DATASET_PATH = "data/datasets/UnansweredQuestions/dataset_docs_public.json"
SAVE_DIRECTORY = "data/output/search_results/UnansweredQuestions"

install:
	uv sync

index:
	uv run python3 -m src index --max_chunk_size $(MAX_CHUNK_SIZE)

search:
	uv run python3 -m src search "$(QUERY)" --k $(K)

search_dataset:
	uv run python3 -m src search_dataset --dataset_path "$(DATASET_PATH)" --k $(K) --save_directory "$(SAVE_DIRECTORY)"
