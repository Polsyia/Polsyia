<div align="center">

<img src="https://github.com/user-attachments/assets/9f00391c-f360-49b3-809a-8d53c5a0731f" width="100%" alt="Banner"/>

# Hi, I'm Musa Emre Delen

**Computer Engineer** · **AI Researcher @ i-LAB, İstinye University** · **Frontend Developer @ Pievision**

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1200&color=0D9488&center=true&vCenter=true&width=640&lines=Turkish+clinical+NLP+for+breast+cancer;Training+domain-specific+language+models;LLM+%26+RAG+for+clinical+decision+support;Building+production+UIs+with+React+%26+Next.js" alt="Turkish clinical NLP for breast cancer · Domain-specific language models · LLM & RAG for clinical decision support · Production UIs with React & Next.js" />

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/musaemredelen)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:musadelen46@gmail.com)

</div>

---

## About me

I'm a Computer Engineering graduate working where **AI meets healthcare**. At **i-LAB (İstinye University)** I'm building a **Turkish clinical NLP for breast cancer**: domain-specific language models that read pathology, radiology and anamnesis reports and power a clinical decision support system. English clinical NLP is a mature field with dedicated biomedical models; Turkish has no equivalent for breast cancer reports yet, and that's the gap we're filling.

Alongside research, I work as a **Frontend Developer at Pievision**, building an e-commerce and warehouse management admin panel with Next.js and TypeScript. Shipping production software every day keeps my research grounded: I care about systems that clinicians can actually use, not just models that score well.

## Current focus

- **Turkish breast cancer NLP:** domain-adaptive pretraining and NER fine-tuning on Turkish pathology, radiology and anamnesis reports, compared against general-purpose models.
- **LLMs in clinical decision making:** comparing rule-based, prompt-based, RAG-based and LLM-only decision strategies on the same patient data.
- **Trustworthy medical AI:** de-identification, reproducible model versions and clinician-in-the-loop feedback.
- **Also exploring:** medical image processing, especially ultrasound/DICOM pipelines for liver imaging.

---

## Featured research: CDSSAI, a Turkish clinical NLP for breast cancer

*i-LAB, İstinye University* · *ongoing, paper in preparation*

Breast cancer care runs on free-text reports: pathology, radiology and anamnesis notes, full of abbreviations, Latin terms and negations. English has a mature ecosystem of clinical and biomedical language models for this kind of text; **Turkish has no equivalent for breast cancer reports**. CDSSAI fills that gap with **domain-specific Turkish language models trained on breast cancer reports**, and uses them as the foundation of a clinical decision support system.

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

**AI / ML**<br/>
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

**Frontend**<br/>
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?style=for-the-badge&logo=reactquery&logoColor=white)

**Backend & data**<br/>
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)

**Tools**<br/>
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

---

## GitHub activity

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=Polsyia&show_icons=true&hide_border=true&include_all_commits=true&bg_color=00000000&title_color=2DD4BF&icon_color=2DD4BF&text_color=C9D1D9" />
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=Polsyia&show_icons=true&hide_border=true&include_all_commits=true&bg_color=00000000&title_color=0D9488&icon_color=0D9488&text_color=1F2328" alt="GitHub stats for Polsyia" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=Polsyia&hide_border=true&background=00000000&ring=2DD4BF&fire=2DD4BF&currStreakLabel=2DD4BF&currStreakNum=C9D1D9&sideNums=C9D1D9&sideLabels=C9D1D9&dates=8B949E&stroke=30363D" />
  <img height="165" src="https://streak-stats.demolab.com?user=Polsyia&hide_border=true&background=00000000&ring=0D9488&fire=0D9488&currStreakLabel=0D9488&currStreakNum=1F2328&sideNums=1F2328&sideLabels=1F2328&dates=59636E&stroke=D0D7DE" alt="GitHub contribution streak for Polsyia" />
</picture>

</div>

---

<div align="center">

![Profile views](https://komarev.com/ghpvc/?username=Polsyia&color=0d9488&style=flat-square&label=Profile+views)

*"Dream big. Start small. Act now."*

</div>
