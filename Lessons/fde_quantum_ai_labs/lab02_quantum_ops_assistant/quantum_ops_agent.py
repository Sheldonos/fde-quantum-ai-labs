#!/usr/bin/env python3
"""
IBM Forward Deployed Engineering - Lab 02: Quantum Job Operations Assistant & FinOps Governor
Integrates IBM Quantum REST API with Pre-flight Validation and AI Triage
"""

import os
import time
import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Multi-tenant Team Budget Allocation Store (in QPU Seconds)
BUDGET_STORE = {
    "TEAM-QUANTUM-CHEM": {"allocated_seconds": 3600.0, "consumed_seconds": 2450.0},
    "TEAM-FIN-RISK": {"allocated_seconds": 1800.0, "consumed_seconds": 1780.0},
    "TEAM-SUPPLY-CHAIN": {"allocated_seconds": 1200.0, "consumed_seconds": 300.0}
}

class QuantumJobSubmission(BaseModel):
    team_id: str
    program_id: str = "sampler"  # sampler | estimator
    backend_name: str = "ibm_fez"
    num_qubits: int = Field(..., ge=1, le=156)
    circuit_depth: int
    shots: int = 4096
    isa_verified: bool = True
    project_crn: Optional[str] = None

class BudgetGovernor:
    @staticmethod
    def check_and_reserve_budget(team_id: str, estimated_qpu_seconds: float) -> bool:
        if team_id not in BUDGET_STORE:
            console.print(f"[bold red]Access Denied:[/bold red] Team '{team_id}' not registered in FinOps policy.")
            return False
        
        record = BUDGET_STORE[team_id]
        remaining = record["allocated_seconds"] - record["consumed_seconds"]
        
        if remaining < estimated_qpu_seconds:
            console.print(
                f"[bold red]❌ FinOps Hard-Lock Triggered:[/bold red] Team '{team_id}' requested {estimated_qpu_seconds:.1f}s, "
                f"but only [bold yellow]{remaining:.1f}s[/bold yellow] remain in allocation quota!"
            )
            return False
        
        # Reserve estimate
        record["consumed_seconds"] += estimated_qpu_seconds
        usage_pct = (record["consumed_seconds"] / record["allocated_seconds"]) * 100.0
        console.print(f"[green]✔ Budget Approved:[/green] {estimated_qpu_seconds:.2f}s reserved. "
                      f"Team {team_id} utilization: [bold yellow]{usage_pct:.1f}%[/bold yellow] "
                      f"(Remaining: {record['allocated_seconds'] - record['consumed_seconds']:.1f}s)")
        return True

class FailureDiagnosticReasoner:
    COMMON_ERRORS = {
        "ERR_NON_ISA_GATES": {
            "root_cause": "Circuit contains non-basis gates (e.g. multi-controlled gates or un-decomposed SWAPs).",
            "fix": "Run generate_preset_pass_manager(optimization_level=3, backend=backend).run(circuit) before dispatch."
        },
        "ERR_COUPLING_VIOLATION": {
            "root_cause": "Two-qubit gate placed across disconnected physical qubits on the backend heavy-hex topology.",
            "fix": "Ensure pass manager includes physical qubit routing and transpiled layout mapping."
        },
        "ERR_QPU_TIMEOUT": {
            "root_cause": "Job execution exceeded maximum allowed time slice on physical device.",
            "fix": "Reduce shot count (e.g., from 100k to 4096) or fragment deep circuit via circuit cutting."
        }
    }

    @classmethod
    def diagnose_failure(cls, raw_error_code: str) -> Dict[str, str]:
        if raw_error_code in cls.COMMON_ERRORS:
            return cls.COMMON_ERRORS[raw_error_code]
        return {
            "root_cause": "Uncategorized runtime or hardware queue exception.",
            "fix": "Inspect backend status via GET /v1/backends/{backend_name}/status and verify API token CRN scope."
        }

class QuantumOpsAssistant:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("IBM_QUANTUM_API_KEY", "mock_key_42")
        self.base_url = "https://api.quantum.cloud.ibm.com/v1"

    def pre_flight_check(self, job: QuantumJobSubmission) -> tuple[bool, str]:
        # Validate Qubit count
        if job.num_qubits > 156:
            return False, "ERR_QUBIT_OVERFLOW: Heron backends support up to 156 physical qubits."
        if not job.isa_verified:
            return False, "ERR_NON_ISA_GATES"
        if job.circuit_depth > 500:
            return False, "ERR_DEPTH_EXCEEDED: Circuit depth exceeds coherent fidelity threshold for NISQ execution."
        return True, "PREFLIGHT_PASSED"

    def submit_and_track_job(self, job: QuantumJobSubmission):
        console.print(f"[bold cyan]▶ Ingesting Job Request:[/bold cyan] Team: [yellow]{job.team_id}[/yellow] | "
                      f"Backend: [green]{job.backend_name}[/green] | Qubits: {job.num_qubits} | Depth: {job.circuit_depth}")
        
        # 1. Pre-Flight Validation
        valid, status_code = self.pre_flight_check(job)
        if not valid:
            console.print(f"[bold red]❌ Pre-Flight Check Failed:[/bold red] {status_code}")
            diagnosis = FailureDiagnosticReasoner.diagnose_failure(status_code)
            console.print(f"  [bold]Root Cause:[/bold] {diagnosis['root_cause']}")
            console.print(f"  [bold green]Recommended Action:[/bold green] {diagnosis['fix']}\n")
            return False

        # 2. Budget Approval
        est_seconds = (job.circuit_depth * 0.005) + (job.shots * 0.0008)
        if not BudgetGovernor.check_and_reserve_budget(job.team_id, est_seconds):
            console.print()
            return False

        # 3. Job Dispatch Simulation
        job_id = f"job-{uuid.uuid4().hex[:12]}"
        console.print(f"[cyan]  ➜ Dispatching PUB payload to {job.backend_name}... Assigned ID: [bold]{job_id}[/bold][/cyan]")
        
        # 4. Polling Lifecycle Simulation
        states = ["QUEUED", "RUNNING", "COMPLETED"]
        for st in states:
            time.sleep(0.15)
            console.print(f"    [dim]• Status:[/dim] [bold blue]{st}[/bold blue] (Target: {job.backend_name})")

        console.print(f"[bold green]✔ Job {job_id} successfully executed! Results retrieved and archived in Factsheet.[/bold green]\n")
        return True

def main():
    console.print(Panel.fit(
        "[bold white on blue] IBM Quantum Job Operations Assistant & FinOps Governor [/bold white on blue]\n"
        "Active Policy: Heron 156Q Cluster | Quota Enforcement: Hard Cap | Pre-flight: Level 3 ISA"
    ))

    assistant = QuantumOpsAssistant()
    
    console.print("[bold yellow]--- Scenario 1: Valid Chemistry VQE Job ---[/bold yellow]")
    valid_job = QuantumJobSubmission(
        team_id="TEAM-QUANTUM-CHEM",
        backend_name="ibm_fez",
        num_qubits=12,
        circuit_depth=48,
        shots=4096,
        isa_verified=True
    )
    assistant.submit_and_track_job(valid_job)

    console.print("[bold yellow]--- Scenario 2: Rejected Non-ISA Job ---[/bold yellow]")
    invalid_job = QuantumJobSubmission(
        team_id="TEAM-SUPPLY-CHAIN",
        backend_name="ibm_marrakesh",
        num_qubits=24,
        circuit_depth=60,
        shots=4096,
        isa_verified=False
    )
    assistant.submit_and_track_job(invalid_job)

    console.print("[bold yellow]--- Scenario 3: FinOps Budget Exceeded ---[/bold yellow]")
    overbudget_job = QuantumJobSubmission(
        team_id="TEAM-FIN-RISK",
        backend_name="ibm_fez",
        num_qubits=40,
        circuit_depth=200,
        shots=50000,
        isa_verified=True
    )
    assistant.submit_and_track_job(overbudget_job)

    # Budget Overview Table
    table = Table(title="Enterprise Team QPU Budget Utilization")
    table.add_column("Research Squad", style="cyan")
    table.add_column("Allocated (s)", style="magenta")
    table.add_column("Consumed (s)", style="yellow")
    table.add_column("Remaining (s)", style="green")
    table.add_column("Utilization Status", style="bold white")

    for team, data in BUDGET_STORE.items():
        rem = data["allocated_seconds"] - data["consumed_seconds"]
        pct = (data["consumed_seconds"] / data["allocated_seconds"]) * 100.0
        status = "HEALTHY" if pct < 80 else ("WARNING" if pct < 95 else "HARD-LOCKED")
        table.add_row(team, f"{data['allocated_seconds']:.1f}", f"{data['consumed_seconds']:.1f}", f"{rem:.1f}", f"{pct:.1f}% ({status})")

    console.print(table)

if __name__ == "__main__":
    main()
