"""
EduTrack AI - Progress Calculation Script
Calculates completion progress (completed_tasks / total_tasks * 100)
for academic subjects based on their associated tasks via CRUD endpoints.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests

def load_env() -> None:
    """Loads environment variables from .env located at project root."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key:
                        os.environ[key] = val

def calculate_progress_metrics(
    tasks: List[Dict[str, Any]], 
    subject_id: Optional[int] = None, 
    subject_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Computes progress metrics from a list of tasks.
    Formula: (completed_tasks / total_tasks) * 100
    Safe zero division handling: returns 0.0 if total_tasks == 0.
    """
    if subject_id is not None:
        filtered = [t for t in tasks if t.get("subject_id") == subject_id]
    else:
        filtered = tasks

    total = len(filtered)
    completed = sum(1 for t in filtered if t.get("status") == "completed")
    pending = total - completed
    percentage = round((completed / total) * 100, 2) if total > 0 else 0.0

    return {
        "subject_id": subject_id,
        "subject_name": subject_name,
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "progress_percentage": percentage
    }

def get_config(key: str, default: str = "") -> str:
    """Retrieves configuration from st.secrets if running in Streamlit, otherwise os.environ/env."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).rstrip("/")
    except Exception:
        pass
    load_env()
    return os.environ.get(key, default).rstrip("/")

def get_auth_headers(token: Optional[str] = None) -> Dict[str, str]:
    """Constructs authorization headers using passed token or environment variables."""
    auth_token = token or get_config("EDUTRACK_AUTH_TOKEN") or get_config("XANO_AUTH_TOKEN")
    return {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

def fetch_subjects(token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves subjects from GET /subjects CRUD endpoint."""
    base_url = (
        get_config("XANO_SUBJECTS_BASE_URL")
        or get_config("XANO_API_BASE_URL")
        or get_config("XANO_AUTH_BASE_URL", "")
    ).rstrip("/")
    if not base_url:
        return []
    try:
        headers = get_auth_headers(token)
        resp = requests.get(f"{base_url}/subjects", headers=headers, timeout=10)
        if resp.status_code == 200 and isinstance(resp.json(), list):
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return []

def fetch_tasks(token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves academic tasks from GET /academic_tasks CRUD endpoint."""
    base_url = (
        get_config("XANO_TASKS_BASE_URL")
        or get_config("XANO_API_BASE_URL")
        or get_config("XANO_AUTH_BASE_URL", "")
    ).rstrip("/")
    if not base_url:
        return []
    try:
        headers = get_auth_headers(token)
        resp = requests.get(f"{base_url}/academic_tasks", headers=headers, timeout=10)
        if resp.status_code == 200 and isinstance(resp.json(), list):
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return []

def calculate_subject_progress(
    subject_id: int, 
    token: Optional[str] = None, 
    tasks_data: Optional[List[Dict[str, Any]]] = None, 
    subjects_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Calculates progress for a specific subject by fetching from CRUD endpoints or using provided data.
    Returns structured dictionary ready for JSON serialization.
    """
    subjects = subjects_data if subjects_data is not None else fetch_subjects(token)
    tasks = tasks_data if tasks_data is not None else fetch_tasks(token)

    subject_name = None
    for s in subjects:
        if s.get("id") == subject_id:
            subject_name = s.get("name")
            break

    return calculate_progress_metrics(tasks, subject_id=subject_id, subject_name=subject_name)

def calculate_all_progress(
    token: Optional[str] = None, 
    tasks_data: Optional[List[Dict[str, Any]]] = None, 
    subjects_data: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Calculates progress for all subjects.
    """
    subjects = subjects_data if subjects_data is not None else fetch_subjects(token)
    tasks = tasks_data if tasks_data is not None else fetch_tasks(token)

    results = []
    for s in subjects:
        s_id = s.get("id")
        s_name = s.get("name")
        metrics = calculate_progress_metrics(tasks, subject_id=s_id, subject_name=s_name)
        results.append(metrics)
    return results

def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate subject academic progress from task completion.")
    parser.add_argument("--subject-id", type=int, help="Optional ID of specific subject to calculate progress for")
    parser.add_argument("--token", type=str, help="Authentication bearer token for Xano endpoints")
    args = parser.parse_args()

    if args.subject_id:
        output = calculate_subject_progress(args.subject_id, token=args.token)
    else:
        output = calculate_all_progress(token=args.token)

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

