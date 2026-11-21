"""
EduTrack AI - Academic Performance PDF Report Generator
Generates a structured, professional PDF document summarizing student academic
progress across subjects and tasks using fpdf2.
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from fpdf import FPDF
import requests

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.calculate_progress import (
    load_env,
    get_config,
    get_auth_headers,
    calculate_all_progress,
    fetch_subjects,
    fetch_tasks
)

class PerformanceReportPDF(FPDF):
    """Custom FPDF class for EduTrack AI Academic Performance Reports."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Header banner
        self.set_fill_color(30, 41, 59)  # Slate dark
        self.rect(0, 0, 210, 28, "F")

        # Title
        self.set_xy(10, 8)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(190, 8, "EduTrack AI - Relatorio de Desempenho", align="L", ln=True)

        self.set_xy(10, 16)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(203, 213, 225)
        self.cell(190, 6, "Gestao Academica Inteligente", align="L", ln=True)

        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        page_str = f"Pagina {self.page_no()}"
        self.cell(0, 10, page_str, align="C")

def build_pdf_document(
    student_name: str,
    student_email: str,
    progress_data: List[Dict[str, Any]],
    output_path: str
) -> str:
    """
    Renders the PDF document using fpdf2 and saves it to output_path.
    """
    pdf = PerformanceReportPDF()
    pdf.add_page()

    # Meta information section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "Identificacao do Estudante", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(95, 6, f"Nome: {student_name}", ln=False)
    pdf.cell(95, 6, f"E-mail: {student_email}", ln=True)

    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(95, 6, f"Data de Emissao: {now_str}", ln=True)
    pdf.ln(4)

    # Calculate overall metrics
    total_subjects = len(progress_data)
    total_tasks = sum(item.get("total_tasks", 0) for item in progress_data)
    total_completed = sum(item.get("completed_tasks", 0) for item in progress_data)
    total_pending = sum(item.get("pending_tasks", 0) for item in progress_data)
    overall_percentage = round((total_completed / total_tasks * 100), 2) if total_tasks > 0 else 0.0

    # Calculate overall average grade from progress_data
    graded_items = [
        item for item in progress_data
        if item.get("average_grade") is not None and item.get("graded_tasks", 0) > 0
    ]
    total_graded_tasks = sum(item.get("graded_tasks", 0) for item in graded_items)
    if total_graded_tasks > 0:
        total_grade_sum = sum(item["average_grade"] * item.get("graded_tasks", 0) for item in graded_items)
        overall_avg_val = round(total_grade_sum / total_graded_tasks, 1)
        overall_avg_str = f"{overall_avg_val:.1f}"
    else:
        # Fallback if average_grade is provided directly without graded_tasks
        simple_grades = [item["average_grade"] for item in progress_data if item.get("average_grade") is not None]
        if simple_grades:
            overall_avg_str = f"{(sum(simple_grades) / len(simple_grades)):.1f}"
        else:
            overall_avg_str = "-"

    # Summary Metrics Cards
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "Resumo Executivo", ln=True)

    # 5 metric boxes
    box_w = 36
    box_h = 18
    gap = 2.5
    start_x = 10
    start_y = pdf.get_y()

    cards = [
        ("Disciplinas", str(total_subjects), (241, 245, 249)),
        ("Total Tarefas", str(total_tasks), (241, 245, 249)),
        ("Concluidas", str(total_completed), (220, 252, 231)),  # Light green
        ("Media Geral", overall_avg_str, (254, 243, 199)),     # Light amber
        ("Progresso Geral", f"{overall_percentage}%", (219, 234, 254))  # Light blue
    ]

    for i, (label, val, fill_rgb) in enumerate(cards):
        x = start_x + (i * (box_w + gap))
        pdf.set_xy(x, start_y)
        pdf.set_fill_color(*fill_rgb)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(x, start_y, box_w, box_h, "DF")

        # Label
        pdf.set_xy(x, start_y + 2)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(box_w, 4, label, align="C")

        # Value
        pdf.set_xy(x, start_y + 7)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(box_w, 7, val, align="C")

    pdf.set_y(start_y + box_h + 8)

    # Detailed Table of Subjects
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "Desempenho Detalhado por Disciplina", ln=True)

    # Table Header
    cols = [
        ("Disciplina", 65),
        ("Total Tarefas", 25),
        ("Concluidas", 25),
        ("Pendentes", 25),
        ("Media", 25),
        ("Progresso", 25)
    ]

    pdf.set_fill_color(51, 65, 85)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    for title, width in cols:
        pdf.cell(width, 8, title, border=1, align="C", fill=True)
    pdf.ln()

    # Table Rows
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)

    if not progress_data:
        pdf.cell(190, 8, "Nenhuma disciplina cadastrada.", border=1, align="C")
        pdf.ln()
    else:
        for idx, item in enumerate(progress_data):
            subj_name = item.get("subject_name") or f"Disciplina #{item.get('subject_id')}"
            tasks_tot = str(item.get("total_tasks", 0))
            tasks_comp = str(item.get("completed_tasks", 0))
            tasks_pend = str(item.get("pending_tasks", 0))
            avg_grade = f"{item['average_grade']:.1f}" if item.get("average_grade") is not None else "-"
            prog_str = f"{item.get('progress_percentage', 0.0)}%"

            fill_row = (idx % 2 == 1)
            pdf.set_fill_color(248, 250, 252) if fill_row else pdf.set_fill_color(255, 255, 255)

            pdf.cell(65, 7, f" {subj_name[:30]}", border=1, align="L", fill=True)
            pdf.cell(25, 7, tasks_tot, border=1, align="C", fill=True)
            pdf.cell(25, 7, tasks_comp, border=1, align="C", fill=True)
            pdf.cell(25, 7, tasks_pend, border=1, align="C", fill=True)
            pdf.cell(25, 7, avg_grade, border=1, align="C", fill=True)
            pdf.cell(25, 7, prog_str, border=1, align="C", fill=True)
            pdf.ln()

    # Save to file
    out_dir = Path(output_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return str(Path(output_path).resolve())

def fetch_report_data_from_endpoint(token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves consolidated report data directly from GET /reports/performance_pdf if available."""
    base_url = (
        get_config("XANO_REPORTS_BASE_URL")
        or get_config("XANO_API_BASE_URL")
        or get_config("XANO_AUTH_BASE_URL", "")
    ).rstrip("/")
    if not base_url:
        return None
    try:
        headers = get_auth_headers(token)
        resp = requests.get(f"{base_url}/reports/performance_pdf", headers=headers, timeout=10)
        if resp.status_code == 200 and isinstance(resp.json(), dict):
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return None

def generate_performance_pdf(
    student_name: str = "Estudante",
    student_email: str = "estudante@edutrack.ai",
    token: Optional[str] = None,
    output_path: str = "reports/relatorio_desempenho.pdf",
    progress_data: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Coordinates data retrieval and PDF generation.
    Returns absolute path of the generated PDF.
    """
    if progress_data is None:
        load_env()
        # Attempt to use GET /reports/performance_pdf first
        endpoint_data = fetch_report_data_from_endpoint(token=token)
        if endpoint_data and "subjects" in endpoint_data and "tasks" in endpoint_data:
            from scripts.calculate_progress import calculate_all_progress
            progress_data = calculate_all_progress(
                token=token,
                tasks_data=endpoint_data.get("tasks", []),
                subjects_data=endpoint_data.get("subjects", [])
            )
        else:
            progress_data = calculate_all_progress(token=token)

    return build_pdf_document(
        student_name=student_name,
        student_email=student_email,
        progress_data=progress_data,
        output_path=output_path
    )

def main():
    parser = argparse.ArgumentParser(description="Generate PDF Academic Performance Report.")
    parser.add_argument("--name", type=str, default="Estudante", help="Student name")
    parser.add_argument("--email", type=str, default="estudante@edutrack.ai", help="Student email")
    parser.add_argument("--output", type=str, default="reports/relatorio_desempenho.pdf", help="Output PDF file path")
    parser.add_argument("--token", type=str, help="Xano auth token")
    args = parser.parse_args()

    saved_path = generate_performance_pdf(
        student_name=args.name,
        student_email=args.email,
        token=args.token,
        output_path=args.output
    )
    print(f"Relatório PDF gerado com sucesso em: {saved_path}")

if __name__ == "__main__":
    main()
