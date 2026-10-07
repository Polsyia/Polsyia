<div align="center">

<img src="assets/banner.svg" width="100%" alt="Musa Emre Delen: Turkish clinical NLP, medical AI, frontend"/>

**Computer Engineer** · **AI Researcher @ i-LAB** · **Frontend Developer @ Pievision**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1200&color=60A5FA&center=true&vCenter=true&width=640&lines=Turkish+clinical+NLP+for+breast+cancer;Training+domain-specific+language+models;LLM+%26+RAG+for+clinical+decision+support;Building+production+UIs+with+React+%26+Next.js" />
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1200&color=1D4ED8&center=true&vCenter=true&width=640&lines=Turkish+clinical+NLP+for+breast+cancer;Training+domain-specific+language+models;LLM+%26+RAG+for+clinical+decision+support;Building+production+UIs+with+React+%26+Next.js" alt="Turkish clinical NLP for breast cancer · Domain-specific language models · LLM & RAG for clinical decision support · Production UIs with React & Next.js" />
</picture>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/musaemredelen)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:musadelen46@gmail.com)

</div>

---

## About me

I'm a Computer Engineering graduate working where **AI meets healthcare**. At **i-LAB** I'm building a **Turkish clinical NLP for breast cancer**: domain-specific language models that read pathology, radiology and anamnesis reports and power a clinical decision support system. English clinical NLP is a mature field with dedicated biomedical models; Turkish has no equivalent for breast cancer reports yet, and that's the gap we're filling.

Alongside research, I work as a **Frontend Developer at Pievision**, building an e-commerce and warehouse management admin panel with Next.js and TypeScript. Shipping production software every day keeps my research grounded: I care about systems that clinicians can actually use, not just models that score well.

## Current focus

- **Turkish breast cancer NLP:** domain-adaptive pretraining and NER fine-tuning on Turkish pathology, radiology and anamnesis reports, compared against general-purpose models.
- **LLMs in clinical decision making:** comparing rule-based, prompt-based, RAG-based and LLM-only decision strategies on the same patient data.
- **Trustworthy medical AI:** de-identification, reproducible model versions and clinician-in-the-loop feedback.
- **Also exploring:** medical image processing, especially ultrasound/DICOM pipelines for liver imaging.

---

## Featured research: CDSSAI, a Turkish clinical NLP for breast cancer

Breast cancer care runs on free-text reports: pathology, radiology and anamnesis notes, full of abbreviations, Latin terms and negations. English has a mature ecosystem of clinical and biomedical language models for this kind of text; **Turkish has no equivalent for breast cancer reports**. CDSSAI fills that gap with **domain-specific Turkish language models trained on breast cancer reports**, and uses them as the foundation of a clinical decision support system.

<p align="center">
  <img src="assets/ner-demo.svg" width="100%" alt="Animated demo: a synthetic Turkish pathology sentence is tagged by the NER model and turned into structured breast cancer findings"/>
</p>

**What the NLP extracts**

| Report type | Key findings |
| --- | --- |
| Pathology | tumor size, histological grade, ER / PR / HER2, lymph node status, TNM |
| Radiology | BI-RADS category, lesion size, location and echo pattern |
| Anamnesis | complaints, family history, reproductive history, age |

**How it's built**

- **Domain-specific language models:** a Turkish BERT + CRF NER model with 14 clinical entity types, including *present / absent* assertion labels so negations like "no malignancy" aren't read as findings.
- **Three-stage adaptation:** general clinical DAPT → report-type DAPT → NER fine-tuning, with separate models for pathology, radiology and anamnesis, benchmarked against general-purpose Turkish models.
- **Clinical post-processing:** links biomarkers to their values, attaches lymph-node context and normalizes grade, BI-RADS and TNM into structured fields.
- **Clinician-in-the-loop:** doctors' corrections are stored as new training data for the next iteration (active learning).
- **Privacy by design:** reports are de-identified before processing, and patient identifiers are encrypted and hashed.

```mermaid
flowchart LR
    A["Turkish reports<br/>PDF / DOCX"] --> B["OCR +<br/>de-identification"]
    B --> C["Domain-specific NER<br/>pathology · radiology · anamnesis"]
    C --> D["Structured<br/>breast cancer findings"]
    D --> E["Risk models<br/>Gail · NPI · PREDICT"]
    D --> F["Decision support<br/>rules · prompting · RAG · LLM"]
    F --> G["Clinician review"]
    G -. "corrections" .-> C
```

**On top of the NLP:** structured findings feed established risk models (Gail, NPI, PREDICT) and a decision layer where rule-based, prompt-based, guideline-grounded RAG and LLM-only strategies make the same decision from the same input, so we can measure which approach actually decides correctly.

<sub>Stack: Python · Django · PyTorch · Hugging Face Transformers · EasyOCR · PyMuPDF · pytest + CI</sub>

---

## Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,pytorch,tensorflow,sklearn,django,nodejs,mysql,cpp&perline=8" alt="Python, PyTorch, TensorFlow, scikit-learn, Django, Node.js, MySQL, C++"/>
  <br/>
  <img src="https://skillicons.dev/icons?i=react,nextjs,ts,tailwind,git,docker,linux,vscode&perline=8" alt="React, Next.js, TypeScript, Tailwind CSS, Git, Docker, Linux, VS Code"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Hugging_Face-Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face Transformers"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/TanStack_Query-FF4154?style=flat-square&logo=reactquery&logoColor=white" alt="TanStack Query"/>
</p>

---

## GitHub activity

<div align="center">

<img src="https://raw.githubusercontent.com/Polsyia/Polsyia/output/ecg.svg" width="100%" alt="GitHub activity drawn as a heart monitor: one heartbeat per day for the last six weeks, with weekly contributions, streaks and the 12-month total"/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Polsyia/Polsyia/output/github-snake-dark.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Polsyia/Polsyia/output/github-snake.svg" alt="Snake animation eating the contribution graph" />
</picture>

</div>

---

<div align="center">

![Profile views](https://komarev.com/ghpvc/?username=Polsyia&color=1d4ed8&style=flat-square&label=Profile+views)

*"Dream big. Start small. Act now."*

</div>

<img src="assets/footer.svg" width="100%" alt=""/>
