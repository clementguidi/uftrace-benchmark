BENCHMARK_APP_SOURCE_DIR=$BENCHMARK_APP_DIR/source

function app_get_url_list {
    csv_file="$1"
    tail -n +2 "$csv_file" \
        | awk -F, '{print $2}'
}

function app_download {
    app_url="$1"
    wget --directory-prefix "$BENCHMARK_APP_SOURCE_DIR" "$app_url"
    # echo $app_url
}

# Reads list of app urls from stdin
function app_download_list {
    while read -r url
    do
        app_download "$url"
    done
}

function app_download_all {
    app_get_url_list "$BENCHMARK_APP_DIR/list.csv" \
        | app_download_list
}
