# Property Risk Tracker

A Python + SQLite command-line tool for tracking property risk data, built as a weekend project to prepare for a software engineering co-op application.

## Features
- Add, view, and delete properties (name, location, value, risk category, risk score)
- SQLite database for persistent storage
- Risk analysis using pandas: calculates risk exposure (value × risk score) and ranks properties
- Unit tests for core logic

## Why these technical choices
- **SQLite**: practiced relational database and SQL skills
- **OOP (Property class)**: models real-world entities cleanly
- **pandas**: added a lightweight data analytics feature
- **unittest**: automated testing instead of manual checking

## Tech stack
Python, SQLite, pandas, unittest

## How to run
py main.py