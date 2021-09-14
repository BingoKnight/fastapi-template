#!/bin/sh

includes_args=false

# options are mutually exclusive, will only run first arg encountered
while getopts "auih" opt; do
    case ${opt} in
        a )
            includes_args=true
            echo "Running all tests"
            coverage run -m pytest
            ;;
        u)
            includes_args=true
            echo "Running unit tests"
            coverage run -m pytest --ignore=app/tests/api -rP
            ;;
        i )
            includes_args=true
            echo "Running integration tests"
            coverage run -m pytest app/tests/api/ -rP
            ;;
        h )
            includes_args=true
            echo "Usage: ./test.sh [ARG]"
            echo ""
            echo "  -a     Run all tests"
            echo "  -u     Run only unit tests"
            echo "  -i     Run only integration tests"
            ;;
    esac
done

if ! $includes_args ; then
    echo "Running all tests"
    coverage run -m pytest
fi

coverage html

