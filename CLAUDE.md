# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LaTeX thesis template for Wuhan University (WHU) bachelor's degree theses, specifically adapted for the School of Cyber Science and Engineering (国家网络安全学院), class of 2021 (graduating 2025). It is based on whu-thesis 2019, modified to meet 2025 requirements.

## Build Command

**Must use XeLaTeX + BibTeX** — other compilers will error. Full build sequence:

```bash
xelatex main.tex
bibtex main.aux
xelatex main.tex
xelatex main.tex
```

Or use a LaTeX editor with XeLaTeX configured (VS Code with LaTeX Workshop, Overleaf, Sublime Text).

> Two extra `xelatex` passes are required after `bibtex` to resolve cross-references and TOC.

## File Structure

| File/Directory | Purpose |
|---|---|
| `main.tex` | Entry point — cover metadata, includes all pages |
| `whu-bachelor-style.cls` | Custom document class — all formatting, fonts, macros |
| `pages/` | Chapter and section `.tex` files |
| `ref/refs.bib` | BibTeX bibliography |
| `figures/` | Image files (also the `\graphicspath`) |

### pages/ structure

- `abstract.tex` — Chinese and English abstracts (use `cnabstract` / `enabstract` environments)
- `chapter1.tex` – `chapter4.tex` — Main body chapters
- `thanks.tex` — Acknowledgements
- `appendix.tex` — Appendix (use `\appendix` before the first appendix chapter)
- `null.tex` — Blank back page

## Key Macros (from `whu-bachelor-style.cls`)

**Cover page fields** (set in `main.tex` before `\maketitlepage`):
```latex
\ctitle{论文题目}
\cschool{学院名称}
\cmajor{专业名称}
\cauthor{作者姓名}
\cnumber{学号}
\cadvisor{导师姓名\quad 职称}
\cdate{二〇二五年X月}
```

**Page generation commands:**
- `\maketitlepage` — renders the cover page
- `\makestatement` — renders the originality declaration page
- `\makecontents` — renders the TOC and resets page numbering to Arabic

**Abstract environments:**
```latex
\begin{cnabstract}{关键词1；关键词2}  % Chinese keywords separated by ；
...
\end{cnabstract}

\begin{enabstract}{Key1; Key2}  % English keywords separated by ; (space after)
...
\end{enabstract}
```

**Citation:** Use `\cite{key}` for standard citations. Use `\rawcite{key}` for citations that must follow the GB/T 7714 numeric style with square brackets.

## Formatting Rules

- Body text: Songti (宋体), size 小四 (zihao -4), line spacing fixed at 23pt
- Chapter titles: Heiti (黑体) 小二号, centered
- Section (一级): Heiti 4号, left-aligned
- Subsection / subsubsection: Heiti 小四号, left-aligned
- TOC depth: 2 levels (chapter + section)
- Heading numbering depth: 3 levels
- Page margins: left/right 3.17cm, top/bottom 2.54cm
- English font: Times New Roman throughout

## Bibliography

Uses `gbt7714-numerical` style (GB/T 7714 national standard). The `.bib` file is at `ref/refs.bib`. Add entries there and cite with `\cite{}`.

## Compiled Output Files

The following are build artifacts (not tracked in git — add to `.gitignore` if needed):
`main.aux`, `main.log`, `main.out`, `main.pdf`, `main.synctex.gz`, `main.thm`, `main.toc`, `pages/*.aux`
