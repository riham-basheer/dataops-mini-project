
# Containerized DataOps Pipeline

An automated, containerized DataOps pipeline that cleans, validates, and aggregates transaction data. The project features automated CI/CD validation via GitHub Actions and local Infrastructure as Code (IaC) provisioning using Terraform.

---

## Pipeline Architecture


```

data/transactions.csv
         │
         ▼
┌──────────────────┐
│ Validation Layer │ ──► output/invalid_transactions.csv
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Processing &     │ ──► output/valid_transactions.csv
│ Aggregation      │ ──► output/aggregated_transactions.csv
└──────────────────┘

```

---

## Tech Stack

* **Data Processing & Testing:** Python, Pandas, Pytest
* **Containerization:** Docker (`python:3.12-slim`)
* **Infrastructure as Code (IaC):** Terraform (`kreuzwerker/docker` provider)
* **CI/CD:** GitHub Actions

---

## Project Structure


```

├── .github/workflows/
│   └── ci.yml                          # GitHub Actions CI workflow
├── data/
│   └── transactions.csv                # Raw transaction records
├── output/
│   ├── aggregated_transactions.csv     # Metrics aggregated by user
│   ├── invalid_transactions.csv        # Filtered out invalid records
│   └── valid_transactions.csv          # Cleaned & standardized records
├── src/
│   └── transform.py                    # ETL & validation business logic
├── tests/
│   └── test_transform.py               # Automated pytest suite
├── terraform/
│   ├── main.tf                         # Docker provider, image, and container resources
│   ├── variables.tf                    # Configurable parameters (image & container names)
│   ├── outputs.tf                      # Metadata outputs
│   └── versions.tf                     # Provider version constraints
├── .dockerignore
├── .gitignore
├── Dockerfile
└── requirements.txt

```

---

## Execution Guide

### 1. Local Environment (Virtualenv)

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```bash
# Run unit tests
python -m pytest
```
```bash
# Run pipeline
python src/transform.py
```

### 2. Docker Container

```bash
# Build Docker image
docker build -t dataops-pipeline:latest .
```
```bash
# Run batch container
docker run --rm --name dataops-pipeline-container dataops-pipeline:latest

```

### 3. Terraform (Infrastructure as Code)

```bash
cd terraform

# Initialize provider and validate syntax
terraform init
terraform validate
```
```bash
# Provision image and execute batch container
terraform apply -auto-approve

# View container output logs
docker logs dataops-pipeline-container
```
```bash
# Tear down local resources
terraform destroy -auto-approve
```

---

## CI/CD Quality Gates

Every push and pull request to `main`/`master` triggers GitHub Actions to run:

1. **Automated Testing:** Runs `pytest` against data cleaning, transaction validation, and aggregation edge cases.
2. **Docker Build:** Verifies container image compilation without caching discrepancies.
3. **Terraform Checks:** Ensures proper formatting (`terraform fmt -check`), provider initialization (`terraform init`), and schema validation (`terraform validate`).

