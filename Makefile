PYTHON ?= python3
# scripts/run_toolkit.py: wrapper che monkey-patcha duckdb.connect()
# per settare memory_limit e preserve_insertion_order — evita OOM in CI.
TOOLKIT = $(PYTHON) scripts/run_toolkit.py

# --- Anagrafica seeds (eseguire prima dei dataset principali) ---

ANAG_SEEDS = \
	anagrafica/anag-enti \
	anagrafica/anag-comparti \
	anagrafica/anag-qualifiche \
	anagrafica/anag-voci-spesa \
	anagrafica/anag-causali \
	anagrafica/anag-territorio

.PHONY: seeds
seeds:
	@for d in $(ANAG_SEEDS); do \
		echo "=== $$d ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml || exit 1; \
	done

# --- Dataset principali ---

.PHONY: run-occupazione run-assenze run-retribuzioni run-personale
.PHONY: run-flessibili run-contrattazione run-passaggi run-distribuzione
.PHONY: run-all

run-occupazione: extract-dati
	$(TOOLKIT) run all --config occupazione/dataset.yml

run-assenze: extract-dati
	$(TOOLKIT) run all --config assenze/dataset.yml

run-retribuzioni: extract-dati
	$(TOOLKIT) run all --config retribuzioni/dataset.yml

run-personale: extract-dati
	$(TOOLKIT) run all --config personale/dataset.yml

run-flessibili: extract-dati
	$(TOOLKIT) run all --config flessibili/dataset.yml

run-contrattazione: extract-dati
	$(TOOLKIT) run all --config contrattazione/dataset.yml

run-passaggi: extract-dati
	$(TOOLKIT) run all --config passaggi/dataset.yml

run-distribuzione: extract-dati
	$(TOOLKIT) run all --config distribuzione/dataset.yml

run-all: seeds run-occupazione run-assenze run-retribuzioni run-personale \
	run-flessibili run-contrattazione run-passaggi run-distribuzione

# --- Smoke test (--sample-rows 1000, root isolato in out/smoke/) ---

.PHONY: smoke-seeds smoke smoke-occupazione smoke-assenze

smoke-seeds:
	@for d in $(ANAG_SEEDS); do \
		echo "=== $$d (smoke) ==="; \
		$(TOOLKIT) run all --config $$d/dataset.yml --sample-rows 1000 || exit 1; \
	done

smoke-occupazione:
	$(TOOLKIT) run all --config occupazione/dataset.yml --year 2024 --sample-rows 1000

smoke-assenze:
	$(TOOLKIT) run all --config assenze/dataset.yml --year 2024 --sample-rows 1000

smoke: smoke-seeds smoke-occupazione smoke-assenze

# --- Validazione config ---

.PHONY: check
check:
	@for f in $$(find . -path '*/anagrafica/*' -name dataset.yml | sort); do \
		echo "→ $$f"; \
		$(TOOLKIT) inspect paths --config "$$f" --year 2026 > /dev/null 2>&1 || exit 1; \
	done
	@for f in $$(find . -path '*/occupazione/*' -o -path '*/assenze/*' \
		-o -path '*/retribuzioni/*' -o -path '*/personale/*' \
		-o -path '*/flessibili/*' -o -path '*/contrattazione/*' \
		-o -path '*/passaggi/*' -o -path '*/distribuzione/*' \
		-name dataset.yml | sort); do \
		echo "→ $$f"; \
		$(TOOLKIT) inspect paths --config "$$f" --year 2024 > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

# --- Download ZIP annuale (una tantum) ---

.PHONY: download
download:
	python3 scripts/download_zip.py

# --- Estrazione dati dallo ZIP ---

.PHONY: extract-dati
extract-dati:
	@test -f 2024Tutto.zip || { echo "❌ ZIP mancante: fai 'make download' o copia 2024Tutto.zip nella root del repo"; exit 1; }
	unzip -j -o 2024Tutto.zip "2024Dati/*" -d _local/seed/dati/ 2>&1 | tail -1
	@echo "✅ Dati estratti in _local/seed/dati/"

# --- Pulizia ---

.PHONY: clean
clean:
	rm -rf out/data/_runs out/data/probe out/data/raw out/data/clean out/data/mart .tmp/

.PHONY: clean-runs
clean-runs:
	rm -rf out/data/_runs/

# --- Verify output ---

.PHONY: verify
verify:
	$(PYTHON) scripts/verify_output.py --all --year 2024

# --- Help ---

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | sort
