.SILENT: install index search search_dataset

MAX_CHUNK_SIZE = 2000
K = 5
DATASET_PATH = "data/datasets/UnansweredQuestions/dataset_docs_public.json"
SAVE_DIRECTORY = "data/output/search_results/UnansweredQuestions"
DATASET_A_PATH = "data/output/search_results/UnansweredQuestions/dataset_docs_public.json"
SAVE_A_DIRECTORY = "data/output/search_results_and_answer/"

install:
	uv sync

index:
	uv run python3 -m src index --max_chunk_size $(MAX_CHUNK_SIZE)

search:
	uv run python3 -m src search "$(QUERY)" --k $(K)

search_dataset:
	uv run python3 -m src search_dataset --dataset_path "$(DATASET_PATH)" --k $(K) --save_directory "$(SAVE_DIRECTORY)"

answer:
	uv run python3 -m src answer "$(QUERY)" --k $(K)

answer_dataset:
	uv run python3 -m src answer_dataset --dataset_path "$(DATASET_A_PATH)" --save_directory "$(SAVE_A_DIRECTORY)"