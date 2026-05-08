#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[theme]
primaryColor = \"#1f77b4\"
backgroundColor = \"#ffffff\"
secondaryBackgroundColor = \"#f5f7fa\"
textColor = \"#262730\"
font = \"sans serif\"
[client]
headless = true
port = \$PORT
enableXsrfProtection = false
[server]
headless = true
port = \$PORT
enableXsrfProtection = false
" > ~/.streamlit/config.toml
