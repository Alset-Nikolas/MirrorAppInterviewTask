#!/bin/bash

set -x

# Check for correct number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [arg1] [arg2] ..."
    exit 1
fi



gpt-back() {
    source /usr/gpt_back/.env
    alembic upgrade heads
    uvicorn asgi:app --host 0.0.0.0 --port 8080
}


# Execute the function for the given argument
case "$1" in
    gpt-back)
        gpt-back
        ;;
    *)
        echo "Invalid argument"
        exit 1
        ;;
esac
