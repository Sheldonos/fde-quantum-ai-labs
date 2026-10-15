# IBM Forward Deployed Engineering (FDE) & Quantum Solutions: Technical Lab Suite
## Applied AI, OpenShift AI, and IBM Quantum Workshop Series

Welcome to the **IBM FDE Technical Lab Suite**. This 7-lab curriculum is designed for Forward Deployed Engineers, Technical Sales Architects, Quantum Solution Engineers, and Enterprise AI Platform Leads. Each lab bridges high-level strategic use cases with production-ready code, verifiable benchmarks, Kubernetes/OpenShift manifests, and empirical evaluation frameworks.

---

## 🏛 Curriculum Overview & Lab Matrix

| Lab # | Module & Domain | Target Persona & Industry | Executable Project | Core Stack & Tools | Readiness Tier | Primary Success Metric |
|---|---|---|---|---|---|---|
| **Lab 01** | **AI Hardware Portability & Accelerator Benchmarking** | Enterprise IT, AI Platform Engineers (Hybrid Cloud) | [`lab01_hardware_portability/`](lab01_hardware_portability/) | Red Hat OpenShift AI (RHOAI), NVIDIA CUDA, AMD ROCm, vLLM / TGIS, Granite 3.0 / Llama-3 | **Production Build** | Latency (TTFT/TPOT), Throughput (tokens/s), Cost/Task ($) across GPU architectures |
| **Lab 02** | **Quantum Job Operations Assistant & Budget Governor** | Research Leads, Quantum Ops, FinOps | [`lab02_quantum_ops_assistant/`](lab02_quantum_ops_assistant/) | IBM Quantum Platform REST API, Qiskit Runtime V2, FastAPI, SQLite/PostgreSQL, Prometheus | **Production Build** | Zero unauthorized paid runs, 100% transpile layout validation, MTTR for job failures < 2s |
| **Lab 03** | **Molecular Chemistry & Battery Catalyst Copilot** | R&D Scientists, Automotive, Chemicals, Pharma | [`lab03_chemistry_catalyst_copilot/`](lab03_chemistry_catalyst_copilot/) | Qiskit Nature, Sample-based Quantum Diagonalization (SQD), VQE, SparsePauliOp, PySCF/NumPy baseline | **Runnable Research Pilot** | Agreement with Full Configuration Interaction (FCI) $\le 1.6 \times 10^{-3} \text{ Ha}$ (chemical accuracy) |
| **Lab 04** | **Factory Logistics & Dynamic Replanning Agent** | Operations Research, Supply Chain, Manufacturing | [`lab04_factory_replanning_agent/`](lab04_factory_replanning_agent/) | QAOA, QUBO/Ising formulation, OR-Tools (CP-SAT), NetworkX, AerSimulator (ideal/noisy) | **Benchmark Pilot** | Constraint violation rate (0%), Makespan/Cost optimality ratio vs OR-Tools, scaling horizon |
| **Lab 05** | **Portfolio Scenario & Multi-Objective Optimization Workbench** | Quants, Asset Management, Commercial Banking | [`lab05_portfolio_workbench/`](lab05_portfolio_workbench/) | Quantum Approximate Multi-Objective Optimization (QAOA/QAMO), Markowitz Frontier, SciPy SLSQP | **Runnable Research Pilot** | Pareto frontier hypervolume indicator, execution overhead vs classical solver at $N \le 40$ assets |
| **Lab 06** | **Quantum AI-Training Evaluation & FTQC Resource Estimator** | Advanced AI Research, Quantum Algorithms Teams | [`lab06_quantum_ai_training/`](lab06_quantum_ai_training/) | Sparse Backpropagation Simulator, Surface Code Estimator, Clifford+T synthesis models | **Research Engagement** | Fault-tolerant logical qubit count, Magic State Factory footprint, runtime crossover threshold |
| **Lab 07** | **Enterprise Hybrid AI-Quantum Orchestration Engine** | FDE Leads, Solutions Architects, CISO/GRC | [`lab07_hybrid_orchestrator/`](lab07_hybrid_orchestrator/) | watsonx Orchestrate, watsonx.governance, Qiskit Runtime Service, UBI 9, OpenShift Agentic Swarm | **Capstone Production Build** | End-to-end audit traceability, automated human-in-the-loop gate compliance, zero token leakage |

---

## 🚀 Quickstart & One-Click Test Suite

To run the complete suite and verify all 7 labs at once:

```bash
# Execute master test harness
./Lessons/fde_quantum_ai_labs/test_all_labs.sh
```

Or run any individual lab:
```bash
./Lessons/fde_quantum_ai_labs/lab01_hardware_portability/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab02_quantum_ops_assistant/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab03_chemistry_catalyst_copilot/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab04_factory_replanning_agent/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab05_portfolio_workbench/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab06_quantum_ai_training/run_lab.sh
./Lessons/fde_quantum_ai_labs/lab07_hybrid_orchestrator/run_lab.sh
```

---

## 🗺 Detailed Lab Study Guides

- [Lab 01 Guide: AI Hardware Portability & Accelerator Benchmarking on OpenShift AI](./Lab-01-AI-Hardware-Portability-OpenShiftAI.md)
- [Lab 02 Guide: Quantum Job Operations Assistant & Autonomous Budget Governor](./Lab-02-Quantum-Job-Operations-Assistant.md)
- [Lab 03 Guide: Chemistry, Battery & Catalyst Research Copilot (SQD & VQE)](./Lab-03-Chemistry-Battery-Catalyst-Copilot.md)
- [Lab 04 Guide: Factory Logistics & Dynamic Replanning Agent (QAOA vs CP-SAT)](./Lab-04-Factory-Logistics-Replanning-Agent.md)
- [Lab 05 Guide: Portfolio Scenario & Multi-Objective Optimization Workbench](./Lab-05-Portfolio-Scenario-Optimization-Workbench.md)
- [Lab 06 Guide: Quantum AI-Training Evaluation & FTQC Resource Estimation Lab](./Lab-06-Quantum-AI-Training-Resource-Estimation.md)
- [Lab 07 Guide: Enterprise Hybrid AI-Quantum Agentic Workflow Orchestrator](./Lab-07-Enterprise-Hybrid-AI-Quantum-Orchestrator.md)

---
*Built with IBM Quantum, Red Hat OpenShift AI, and watsonx by IBM Forward Deployed Engineering.*
