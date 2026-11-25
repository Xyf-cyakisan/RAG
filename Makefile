.SILENT: install index search search_dataset

MAX_CHUNK_SIZE = 2000
K = 5
DATASET_PATH = "data/datasets/UnansweredQuestions/dataset_docs_public.json"
SAVE_DIRECTORY = "data/output/search_results/UnansweredQuestions"
STUDENT_SEARCH_RESULTS_PATH = "data/output/search_results/UnansweredQuestions/dataset_docs_public.json"
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
	uv run python3 -m src answer_dataset  --student_search_results_path "$(STUDENT_SEARCH_RESULTS_PATH)" --save_directory "$(SAVE_A_DIRECTORY)"

clean:
	rm -rf */*/*/__pycache__
	rm -rf */*/__pycache__
	rm -rf */__pycache__
	rm -rf __pycache__
	rm -rf */*/*/.mypy_cache
	rm -rf */*/.mypy_cache
	rm -rf */.mypy_cache
	rm -rf .mypy_cache
	rm -rf */*/*/.pytest_cache
	rm -rf */*/.pytest_cache
	rm -rf */.pytest_cache
	rm -rf .pytest_cache

fclean: clean
	rm -rf .venv
	rm -rf uv.lock
	uv cache clean

lint:
	uv run python -m flake8 src && printf '\033[1;32mFlake8 all good !\033[0m\n'; uv run python -m mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=silent

lint-strict:
	uv run python -m flake8 src && printf '\033[1;32mFlake8 all good !\033[0m\n'; uv run python -m mypy src --strict --follow-imports=silent