.SILENT: install index

install:
	uv sync

index:
	uv run python3 -m src index $(MAX_CHUNK_SIZE)
