# Agent Backend

This repository contains the backend service for the Financial Coach Agent application.
Backend is a python FastApi application, using Gemini as the LLM.


## Prerequisites

- python3 installed
- Create an .env file with following variables: GEMINI_API_KEY, JSON_SERVER_URL


## Running the backend

1. ```bash
    python3 -m venv ./venv
    ```
2. ```bash
    source ./venv/bin/activate
    ```
3. ```bash
    pip install -r ./requirements.txt
    ```
4. ```bash
    uvicorn main:app --reload
    ```
