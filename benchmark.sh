#!/usr/bin/env bash

set -euo pipefail

echo "# # # # # # # # # # # # # # # # # # #"
echo "# DORSAL's uftrace benchmark suite  #"
echo "#               v0.1                #"
echo "# # # # # # # # # # # # # # # # # # #"

function benchmark_download_applications {
    true
}

function benchmark_build_applications {
    true
}

function benchmark_install_applications {
    true
}

function benchmark_run_test {
    true
}

# options
# --output/-O output dir
# --log log uftrace output
# --success-rate --instrumentation-time --overhead test selection (success rate, overhead, ...)
# --uftrace uftrace location
# download/build test applications (choose flags -g -Ox -pg)

# behaviour

getopt --test > /dev/null && exit 1
if [[ $? -ne 4 ]]
then
    echo "getopt (enhanced) not available"
    exit 1
fi

OPTIONS=O:
LONGOPTIONS=output:,log,success-rate,instrumentation-time,overhead,uftrace:,app-binary-size:,app-function-count:,app-language:

PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]
then
    echo "getopt failed"
    exit 2
fi

eval set -- "$PARSED"

O=results LOGP=n FULLTESTP=y SUCCESSRATEP=n INSTRUMENTATIONTIMEP=n OVERHEADP=n
UFTRACE=$(which uftrace)
while true
do
    case $1 in
        -O|--output)
            O=$2
            shift 2
            ;;
        --log)
            LOGP=y
            shift
            ;;
        --success-rate)
            FULLTESTP=n
            SUCCESSRATEP=y
            shift
            ;;
        --instrumentation-TIME)
            FULLTESTP=n
            INSTRUMENTATIONTIMEP=y
            shift
            ;;
        --overhead)
            FULLTESTP=n
            OVERHEADP=y
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "error parsing options"
            exit 3
    esac
done

# check tests to run

if [[ $# -ge 1 ]]
then
    case $1 in
        download)
            benchmark_download_applications
            ;;
        build)
            benchmark_build_applications
            ;;
        install)
            benchmark_install_applications
            ;;
        test)
            benchmark_run_test
            ;;
        *)
            echo "command $1 undefined"
            exit 1
    esac
else
    benchmark_run_test
fi
