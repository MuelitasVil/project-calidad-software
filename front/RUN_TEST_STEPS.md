# Easy Steps to Run Frontend Tests

## Quick Start (3 Steps)

### Step 1: Start Services
```bash
# From project root
make up
# or
./start-dev.sh
```

### Step 2: Run Tests
Choose one of these methods:

#### Method A: Using the script (Easiest)
```bash
# From project root
# Run all integration tests
./front/run-tests.sh integration
# Run all unit tests
./front/run-tests.sh unit
# Run all end to end tests
./front/run-tests.sh end-to-end
# Run a specific test file
./front/run-tests.sh integration-tests/test_guest_registration_integration.py
# or
./front/run-tests.sh end-to-end-tests/test_guest_registration_and_profile_edit.py
# Run all tests
./front/run-tests.sh all
# or
./front/run-tests.sh
```

#### Method B: Using Make commands
```bash
# From project root
make test-frontend                # All tests
make test-frontend-unit          # Unit tests only
make test-frontend-integration   # Integration tests only
```

#### Method C: Using docker-compose directly
```bash
# From project root
docker compose --profile test run --rm frontend-tests pytest -v
docker compose --profile test run --rm frontend-tests pytest -m unit -v
docker compose --profile test run --rm frontend-tests pytest -m integration -v -s
```

## Complete Example

```bash
# 1. Start services (if not already running)
cd /Users/eri/Projects/project-calidad-software
make up

# 2. Wait a few seconds for services to be ready
sleep 5

# 3. Run tests
./front/run-tests.sh
```

## Troubleshooting

### "docker-compose.yml not found"
- Make sure you're running the script from the project root, or the script will auto-navigate there

### "Frontend service doesn't seem to be running"
- The script will try to start services automatically
- Or manually run: `make up`

### "Connection refused" errors
- Make sure all services are running: `make ps`
- Wait a bit longer for services to be ready: `sleep 10`

### Test container not found
- Build it first: `docker compose --profile test build frontend-tests`

## What Gets Tested

- **Unit Tests**: Individual form components (login, register, profile)
- **Integration Tests**: API endpoints and database verification (no UI)
- **End-to-End Tests**: Complete UI flow with Selenium (register → login → edit profile)

All tests run in Docker - no local dependencies needed!

