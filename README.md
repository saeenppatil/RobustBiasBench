# RobustBiasBench

**RobustBiasBench** is a comprehensive benchmark for evaluating the robustness of large language models (LLMs) in detecting social and systemic biases within real-world policy texts. It introduces both a human-annotated dataset of over 18,000 U.S. policy excerpts and a modular perturbation toolkit (`PERTURBKIT`) designed to simulate real-world noise and adversarial attacks.

---

## Project Overview

- **Goal**: Evaluate and improve the robustness of LLMs in identifying **demographic bias**, **systemic bias**, and **no bias** in formal policy documents, even under noisy or adversarial inputs.
- **Dataset**: 18,404 human-annotated excerpts from U.S. government documents (laws, bills, registers, party platforms, etc.)
- **Classes**:
  - `group_1`: Systemic bias (legal, civic, institutional)
  - `group_2`: Demographic bias (identity, social, economic)
  - `no_bias`: Operational or procedural content
- **Perturbation Types**: Typo noise, gibberish prefixes, whitespace alteration, word order shuffling, synonym substitution, prompt injection.

---

## Repository Structure

```
RobustBiasBench/
│
├── Data/
│   ├── RobustBiasBench Dataset.csv
│   ├── Source License Files/
│       └── BillSum License
│       └── Federal Regsiter License
│       └── SPRC19 License
│       └── Comparative Agendas License
│       └── source_licenses.txt
│
├── Code/
│   ├── Data Curation Code
│       └── scraping and keywords data curation code divided by dataset
│   ├── Models Code
│       └── LLM fewshot and zeroshot evaluation code divided by model
│   ├── PerturbKit Code
│       └── perturbkit.py
│
├── LICENSE
└── README.md
```

---

## Evaluation Protocol

### Models Used

- Meta LLaMA3-8B-Instruct
- DeepSeek-7B-Chat
- Mistral-7B-Instruct
- Qwen-2.5-7B-Instruct
- Phi-4-Mini-Instruct
- Vicuna-7B-v1.5

### Prompting Modes

- **Zero-shot**: Instruction + label definitions
- **Few-shot (9-shot)**: 3 examples from each class included in prompt

### Metrics

- Accuracy
- F1 Score
- Precision
- Recall


---

## Data Sources & Licensing

All datasets are licensed for academic use:

- **Federal Register** – Public Domain
- **Comparative Agendas Project** – CC-BY-NC-SA 4.0
- **BillSum** – CC-BY 4.0 / Apache 2.0
- **SPRC19** – CC0

---

## Limitations

- U.S.-centric dataset — may not generalize internationally
- Rule-based perturbations — future work may incorporate learned adversarial attacks
- Single-label per excerpt — doesn't capture intersectional bias

---

## Contributors

- Akash Bonagiri, Saee Patil, Kevin Xu, Ariana Smith, Gerard Anderias, Andrew Fojas, Winston Yu, Akanksha Bonagiri, Teddy Liu, Setareh Rafatirad

---

## Ethics and Use

This dataset contains excerpts that reference sensitive identities or groups, including but not limited to race, gender, disability, socioeconomic status etc. These texts may reflect biased language present in real-world policy. We **do not endorse** or promote any such biased content; all excerpts are included **solely for research purposes** and should be interpreted within the context of fairness, accountability, and responsible AI development.

---

## Links

- [Codebase](https://github.com/saeenppatil/RobustBiasBench)
- [Dataset Hosting (HuggingFace)](https://huggingface.co/datasets/bsakash/RobustBiasBench)

