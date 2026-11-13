#!/bin/bash
set -e

# ===== Configuration =====
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${POSTGRES_USER:-makedecision}"
DB_NAME="${POSTGRES_DB:-makedecision}"

REDIS_HOST="${REDIS_HOST:-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"

MAX_RETRIES="${WAIT_MAX_RETRIES:-30}"
RETRY_INTERVAL="${WAIT_RETRY_INTERVAL:-2}"

# ===== Helper =====
log() {
    echo "[entrypoint] $1"
}

# ===== Wait for PostgreSQL =====
log "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."

retries=0
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
    retries=$((retries + 1))
    if [ "$retries" -ge "$MAX_RETRIES" ]; then
        log "ERROR: PostgreSQL is not ready after ${MAX_RETRIES} attempts. Exiting."
        exit 1
    fi
    log "PostgreSQL is unavailable (attempt ${retries}/${MAX_RETRIES}) – sleeping ${RETRY_INTERVAL}s..."
    sleep "$RETRY_INTERVAL"
done

log "PostgreSQL is ready."

# ===== Wait for Redis =====
log "Waiting for Redis at ${REDIS_HOST}:${REDIS_PORT}..."

retries=0
until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping 2>/dev/null | grep -q "PONG"; do
    retries=$((retries + 1))
    if [ "$retries" -ge "$MAX_RETRIES" ]; then
        log "ERROR: Redis is not ready after ${MAX_RETRIES} attempts. Exiting."
        exit 1
    fi
    log "Redis is unavailable (attempt ${retries}/${MAX_RETRIES}) – sleeping ${RETRY_INTERVAL}s..."
    sleep "$RETRY_INTERVAL"
done

log "Redis is ready."

# ===== Optional: run migrations only for the backend service =====
if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
    log "Running database migrations..."
    python manage.py migrate --noinput

    log "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# ===== Execute the main command =====
log "Starting: $*"
exec "$@"
