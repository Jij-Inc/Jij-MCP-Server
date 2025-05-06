qiskit_v1_v2_migration_prompt = """# Qiskit v1.0: A New Era of Stability, Performance, and Standardized Interfaces**

Qiskit v1.0, released in February 2024, marked a pivotal moment, shifting from a research-oriented tool with frequent breaking changes (v0.x) to a more stable and performant SDK. Key objectives included API stability through the formal adoption of semantic versioning (X.Y.Z), significant performance enhancements, and the introduction of new standardized interfaces.

**Major Architectural and API Changes in Qiskit 1.0:**

1.  **Package Restructuring:**
    * The `qiskit` meta-package now directly provides the core SDK.
    * Direct dependency on `qiskit-terra` was deprecated, with `qiskit` becoming the recommended dependency.
    * In-place upgrades from v0.x were discouraged, requiring new virtual environments.

2.  **Simulator Separation (`qiskit-aer`):**
    * High-performance simulators (`qiskit.Aer`) were moved out of the core `qiskit` package into a separate, installable package: `qiskit-aer` (`pip install qiskit-aer`).
    * The `qiskit.BasicAer` object (pure Python simulators) was completely removed. Its functionalities were replaced by:
        * `qiskit.providers.basic_provider.BasicProvider` for basic backend provider features.
        * `qiskit.quantum_info` module (e.g., `Statevector`, `Operator`) for statevector and unitary simulations.
        * `qiskit_aer.AerSimulator` for more general and performant simulations.
    * This separation allowed `qiskit-aer` to have its own dependencies (like C++ compilers, CUDA) and release cycle, optimizing it for high-performance simulation.

3.  **Execution Workflow Change (Removal of `execute`):**
    * The global `qiskit.execute` function was removed.
    * The recommended workflow became explicit transpilation using `qiskit.transpile(circuit, backend)` followed by execution using `backend.run(transpiled_circuit)`.
    * Alternatively, Qiskit Primitives (see below) offered a higher-level abstraction for execution.

4.  **QASM Output Change:**
    * The `QuantumCircuit.qasm()` method was removed.
    * OpenQASM 2.0 output is now handled by functions in the `qiskit.qasm2` module (e.g., `qiskit.qasm2.dump()`, `qiskit.qasm2.dumps()`).

5.  **Introduction of Primitives V1 (Sampler & Estimator):**
    * This was a major paradigm shift for how users interact with backends.
    * **Sampler**: Takes circuits as input and returns (quasi-)probability distributions (counts).
    * **Estimator**: Takes circuits and observables as input and returns expectation values.
    * These Primitives aimed to standardize the interface between algorithms and backends (both simulators and real hardware).
    * They effectively replaced the older `QuantumInstance` and `qiskit.opflow` modules, which were deprecated. `qiskit.quantum_info.SparsePauliOp` became the standard for representing observables with the Estimator.

**Ecosystem Reorganization (Qiskit Community Packages):**

* Alongside Qiskit 1.0, functionalities previously part of the monolithic `qiskit-aqua` package were restructured into separate, domain-specific community packages:
    * `qiskit-algorithms` (for core quantum algorithms)
    * `qiskit-nature` (for natural sciences)
    * `qiskit-machine-learning`
    * `qiskit-optimization`
    * `qiskit-finance`
    * `qiskit-experiments` (for characterization, calibration, and benchmarking, succeeding parts of `qiskit-ignis`)
* These packages were updated to be compatible with Qiskit 1.0 and to use the new Primitives V1 interface.

**Evolution through Qiskit 1.x Minor Releases (v1.1 - v1.4):**

* These releases focused on continued performance improvements (largely through deeper Rust integration for core components like circuit operations and transpiler passes), bug fixes, and new features (e.g., typed classical variables in circuits, new transpiler passes, `SparseObservable`).
* Critically, these versions began introducing V2 Primitive backend implementations and added deprecation warnings for features that would be removed in Qiskit 2.0. Qiskit v1.4 served as a "移行リリース" to help users prepare.

**Qiskit v2.0: Modernization, Peak Performance, and Legacy Cleanup (Released March 2025)**

Qiskit 2.0 built upon the foundation of v1.0, further modernizing the SDK, enhancing performance, and streamlining the codebase by removing long-deprecated components.

**Core SDK Evolution in Qiskit 2.0:**

1.  **Deeper Rust Integration & C-API:**
    * More core data structures (e.g., qubit registers, instruction classes) were rewritten in Rust, leading to further speedups (e.g., 2x faster circuit construction compared to v1.3).
    * The first **C language API** was introduced, initially for `SparseObservable`, paving the way for better integration with non-Python environments and HPC.

2.  **New Circuit Features & OpenQASM 3 Alignment:**
    * **Stretch variables** for `Delay` instructions, enabling more abstract representation of timing in dynamic circuits.
    * **`BoxOp` / `box` instruction**, corresponding to OpenQASM 3's `box`, for logical grouping of operations.
    * Enhanced support and alignment with OpenQASM 3 semantics.

3.  **Definitive Removal of Legacy Components:**
    * `qiskit.pulse` module: Completely removed. Pulse-level control is now expected to be handled by tools like Qiskit Dynamics or higher-level abstractions like fractional gates on hardware.
    * `qobj` (Quantum Job Object): Removed.
    * `BackendV1` and related modules (`qiskit.providers.models`): Completely removed. `BackendV2` is now the standard.
    * V1 Primitive reference implementations were removed from the core `qiskit.primitives` module.
    * Other deprecated methods and classes (e.g., legacy `c_if` on instructions, `BooleanExpression`).

**Primitives V2 as the Standard Interface in Qiskit 2.0:**

* Primitives V2 became the standard, refined based on experience with V1.
* **Key Differences from V1:**
    * **Input - Primitive Unified Blocs (PUBs):** V2 Primitives accept a list of PUBs. A PUB groups a single circuit with its associated data (parameters, observables, shots, precision). This provides a more structured and vectorized input mechanism.
        * SamplerV2 PUB: `(circuit, param_values, shots)`
        * EstimatorV2 PUB: `(circuit, observables, param_values, precision)`
    * **Output:**
        * `SamplerV2` returns raw bitstrings (preserving shot order), with convenience methods like `get_counts()`.
        * `EstimatorV2` returns expectation values (`evs`) and standard errors (`stds`) directly in `PubResult.data`.
    * **ISA Circuit Requirement:** A crucial change is that V2 Primitives **require pre-transpiled ISA (Instruction Set Architecture) circuits**. The Primitives themselves do not perform layout, routing, or translation. Users are responsible for transpiling circuits to be compatible with the target backend *before* passing them to V2 Primitives.
    * **Options Handling:** Separate options classes for `SamplerV2` and `EstimatorV2`, using `options.update()` instead of `set_options()`.

**Qiskit Community Packages and Qiskit 2.0:**

* Community packages continued to adapt to the core Qiskit changes.
* This primarily involved adopting Primitives V2 for their algorithms and ensuring compatibility with the removal of `BackendV1`, `qiskit.pulse`, and other legacy components. For instance, `qiskit-machine-learning` updated its QNNs and Kernels to support Primitives V2.

In summary, the transition from Qiskit v0.x through v1.x to v2.0 has been a journey of significant maturation. Qiskit 1.0 laid the groundwork for stability and introduced the Primitives paradigm. Qiskit 2.0 solidified this by making Primitives V2 the standard, demanding more explicit user control over transpilation, and aggressively removing legacy code to create a more streamlined, performant, and modern SDK. Users migrating across these versions need to be particularly aware of the changes in simulation (Aer separation), execution (Primitives V1/V2, ISA circuits), and the removal of major components like `QuantumInstance`, `Opflow`, and `qiskit.pulse`.
"""
