# XXEProbe — XML Security Testing and Analysis Tool

**Developer:** Faizan  
**Institute:** PNY Trainings · **Department:** Cyber Security · **Track:** Web Security  
**Instructor:** Abdul Mannan  
**Version:** 1.1.0

## 1. Project overview

XXEProbe is an educational Python project for learning XML document construction, secure XML input handling, localhost event logging, basic response-text checks, and JSON reporting. All network components bind to `127.0.0.1` only.

**Important scope statement:** this release is a safe localhost XML validation prototype. It does not perform exploit-based XXE verification and must not be described as a complete XXE vulnerability scanner. Marker/error matching and listener logging are self-checks only.

## 2. Features

- Generates benign baseline and marker XML documents.
- Runs a defensive XML receiver on localhost with request-size limits and DTD/entity declaration rejection.
- Runs benign baseline, marker, malformed-XML, and DTD-rejection validation checks against that local receiver.
- Provides heuristic response marker and parser-error-text checks.
- Provides a separate localhost-only HTTP event logger and JSONL audit.
- Generates machine-readable JSON reports with explicit limitations and remediation guidance.
- Includes unit tests for the XML builder and text-analysis functions.

## 3. Requirements

- Python 3.10 or newer recommended.
- Windows CMD or a terminal.
- No third-party packages are required; the project uses the Python standard library.

## 4. Project structure

```text
XXEProbe/
├── main.py
├── config.py
├── payload_builder.py
├── detector.py
├── listener.py
├── listener_audit.py
├── reporter.py
├── requirements.txt
├── README.md
├── .gitignore
├── lab/
│   ├── secure_app.py
│   ├── test_client.py
│   └── analyze_results.py
├── tests/
│   └── test_project.py
└── reports/
    └── .gitkeep
```

Generated JSON/JSONL reports are intentionally excluded from version control by `.gitignore`.

## 5. Setup (Windows CMD)

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

No `pip install` step is needed.

## 6. Run the project

Open CMD in the project folder.

### A. Run component self-check and generate the main report

```cmd
python main.py
```

### B. View configuration

```cmd
python main.py --config
```

### C. Start the defensive localhost XML lab

Terminal 1:

```cmd
python lab\secure_app.py
```

Keep this terminal running. It listens only on `127.0.0.1:8001`.

Terminal 2:

```cmd
python lab\test_client.py
python lab\analyze_results.py
```

The test client expects four outcomes: baseline XML `200`, marker XML `200`, malformed XML `400`, and a harmless DTD declaration rejected with `400`.

### D. Start and audit the separate localhost event logger

Terminal 3:

```cmd
python listener.py
```

The listener binds only to `127.0.0.1:8000`. It records local GET requests as listener events. A listener event proves only that the listener received a request; it is not evidence of an XXE callback.

Terminal 4:

```cmd
python listener_audit.py
```

### E. Run unit tests

```cmd
python -m unittest discover -s tests -v
```

### F. Compile-check Python files

```cmd
python -m compileall -q .
```

## 7. Reports

- `reports/xxe_report.json` — main self-check and listener audit.
- `reports/lab_test_results.json` — individual localhost validation results.
- `reports/final_lab_report.json` — summarized validation outcomes.
- `reports/oob_events.jsonl` — local listener event log.

Reports are generated when their corresponding commands run.

## 8. Limitations and interpretation

- The XML builder creates ordinary XML only; it does not create external-entity exploit documents.
- Marker matching is a text self-test, not proof of entity expansion.
- Parser-error text matching is heuristic and can produce false positives/negatives.
- Local listener events demonstrate listener operation only.
- The included secure lab demonstrates defensive input handling; it is not an intentionally vulnerable target.
- `xxe_confirmed` remains `false` because this release does not verify an XXE exploit condition.

## 9. Defensive recommendations

- Disable DTD processing when it is unnecessary.
- Disable external entity resolution.
- Use a hardened XML parser and keep it updated.
- Enforce request-size limits and validate expected XML structure.
- Test only systems for which explicit authorization has been granted.

## 10. Legal and ethical use

Use this project only in the included localhost lab or another environment you own and are explicitly authorized to assess. Do not direct it at public websites or third-party systems.

## 11. Developer

**Faizan** — Cyber Security Student, PNY Trainings.
