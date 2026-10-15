#!/usr/bin/env python3
"""
IBM Forward Deployed Engineering - Master Test & Lab Suite Runner
Executes and validates all 7 FDE AI, OpenShift, and Quantum Labs
"""

import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

LABS = [
    {
        "id": "Lab 01",
        "title": "AI Hardware Portability & OpenShift AI (NVIDIA vs AMD)",
        "script": "lab01_hardware_portability/benchmark_portability.py",
        "domain": "AI Infrastructure / OpenShift"
    },
    {
        "id": "Lab 02",
        "title": "Quantum Job Operations Assistant & FinOps Budget Governor",
        "script": "lab02_quantum_ops_assistant/quantum_ops_agent.py",
        "domain": "Quantum Ops / FinOps"
    },
    {
        "id": "Lab 03",
        "title": "Chemistry & Battery Catalyst Copilot (SQD & VQE)",
        "script": "lab03_chemistry_catalyst_copilot/chemistry_copilot_sqd.py",
        "domain": "Materials / Chemistry"
    },
    {
        "id": "Lab 04",
        "title": "Factory Logistics Dynamic Replanning (QAOA vs CP-SAT)",
        "script": "lab04_factory_replanning_agent/factory_replanning_bench.py",
        "domain": "Manufacturing / Supply Chain"
    },
    {
        "id": "Lab 05",
        "title": "Portfolio Scenario Optimization Workbench (Multi-Objective QAOA)",
        "script": "lab05_portfolio_workbench/portfolio_workbench.py",
        "domain": "Quantitative Finance"
    },
    {
        "id": "Lab 06",
        "title": "Quantum AI Training & FTQC Resource Estimator",
        "script": "lab06_quantum_ai_training/ftqc_ai_training_estimator.py",
        "domain": "Frontier AI / FTQC"
    },
    {
        "id": "Lab 07",
        "title": "Enterprise Hybrid AI-Quantum Orchestrator (Capstone)",
        "script": "lab07_hybrid_orchestrator/hybrid_orchestrator.py",
        "domain": "Hybrid Agentic Control Plane"
    }
]

def main():
    root_dir = Path(__file__).parent.resolve()
    console.print(Panel.fit(
        "[bold white on blue] IBM Forward Deployed Engineering (FDE) Lab Suite [/bold white on blue]\n"
        "Executing full end-to-end verification of all 7 production labs..."
    ))

    summary_table = Table(title="IBM FDE Lab Execution & Validation Matrix")
    summary_table.add_column("Lab ID", style="cyan", no_wrap=True)
    summary_table.add_column("Domain", style="magenta")
    summary_table.add_column("Lab Title", style="white")
    summary_table.add_column("Runtime", style="yellow")
    summary_table.add_column("Validation Status", style="bold green")

    all_passed = True

    for lab in LABS:
        script_path = root_dir / lab["script"]
        console.print(f"\n[bold cyan]▶ Launching {lab['id']}: {lab['title']}...[/bold cyan]")
        
        start_t = time.perf_counter()
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        elapsed = time.perf_counter() - start_t

        if res.returncode == 0:
            console.print(f"[green]✔ {lab['id']} Passed in {elapsed:.2f}s[/green]")
            summary_table.add_row(
                lab["id"],
                lab["domain"],
                lab["title"],
                f"{elapsed:.2f}s",
                "[bold green]PASSED (100%)[/bold green]"
            )
        else:
            all_passed = False
            console.print(f"[bold red]❌ {lab['id']} Failed:[/bold red]\n{res.stderr}")
            summary_table.add_row(
                lab["id"],
                lab["domain"],
                lab["title"],
                f"{elapsed:.2f}s",
                "[bold red]FAILED[/bold red]"
            )

    console.print("\n", summary_table)

    if all_passed:
        console.print(Panel.fit(
            "[bold green]✔ All 7 Enterprise Labs Built & Verified Successfully![/bold green]\n"
            "Full suite ready for customer demos, FDE workshops, and enterprise architecture pilots.",
            title="Suite Status: ALL GREEN"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]❌ One or more labs encountered errors during execution.[/bold red]",
            title="Suite Status: ACTION REQUIRED"
        ))
        sys.exit(1)

if __name__ == "__main__":
    main()
