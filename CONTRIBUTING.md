# Contributing to CSKnowledgeHub

Thank you for helping improve this knowledge hub. This guide explains scope, style, and the workflow to add or update content.

## About This Repository

This repository contains notes and materials originally curated from **Georgia Tech OMSCS** and **Columbia University** courses, reorganized for exam preparation and interview readiness. We welcome contributions that enhance, correct, or expand upon this foundation while maintaining academic integrity and proper attribution.

## Scope

- Computer Science fundamentals: DS&A, OS, DB, Networks, Machine Learning, Statistics
- Study resources: curated links with brief annotations

Out of scope: full problem dumps, proprietary content, AI-generated dumps without review, framework-specific tutorials, or production/DevOps guides.

## Content style

- Two-level pages: start each page with a 5-minute exam-cram summary (definitions, key formulas, pitfalls). Then provide deeper notes.
- Diagram-first: include at least one diagram for complex topics.
- References: cite sources at the end with title, author, link, and license.
- Worked examples: small, concrete examples (e.g., Gantt chart, EXPLAIN diff, packet walk).
- Tone: concise, neutral, technical. Avoid personal marketing.

## Structure and headings

- Use `#` for page title, then `##` for major sections. Keep a short table of contents if the page is long.
- Prefer consistent section names: Introduction, Key Ideas, Diagram, Worked Example, Pitfalls, Further Reading.
- Use fenced code blocks for snippets. Provide alt-text for images.

## Adding a new topic folder

1. Create a new folder at the root level with a clear name (e.g., `Operating System`, `Database`).
2. Create a `README.md` inside the new folder with a short syllabus and "start here" links.
3. Add topic files with clear names (e.g., `Transport Layer.md`).
4. Update the root `README.md` to include your new topic section.

## Git workflow

- Create a feature branch from `main`.
- If adding content, open an issue first (Content Request) to discuss scope.
- Submit a PR referencing the issue. Fill in the PR checklist.
- Pass CI: markdown lint, spellcheck, and link checker.

## Writing guidelines

- Wrap lines at ~100 characters where reasonable.
- Use lists and tables for scannability; avoid long prose blocks.
- Prefer relative links to repo files; use absolute links for external resources.
- Use English file names. For bilingual files, name `README.en.md` and `README.zh.md` and link them at top.

## Licensing

This project is licensed under Apache License 2.0. By contributing, you agree your contributions will be licensed under the same terms.

## Getting help

Open a Discussion or a Content Request issue if you're unsure about scope or structure.
