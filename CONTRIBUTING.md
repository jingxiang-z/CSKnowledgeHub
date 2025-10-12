# Contributing to CSKnowledgeHub

Thank you for helping improve this **Computer Science Fundamentals Knowledge Hub**. This guide explains scope, style, and the workflow to add or update content.

## About This Repository

CSKnowledgeHub originated from **Georgia Tech** and **Columbia University** computer science courses. Our mission is to provide learners with a **comprehensive view of CS fundamentals**—helping them understand not just individual topics, but the overall structure and interconnections within computer science.

We welcome contributions that enhance, correct, or expand upon this foundation while maintaining academic integrity, clarity, and proper attribution.

## Scope

- **Core Topics**: Data Structures & Algorithms, Computer Architecture, Computer Networks, Operating Systems, Databases, Distributed Systems, Machine Learning, Deep Learning, Natural Language Processing, Information Security, Statistics
- **Study resources**: curated links with brief annotations

Out of scope: full problem dumps, proprietary content, AI-generated dumps without review, framework-specific tutorials, or production/DevOps guides.

## Content Style

- **Structured pages**: Start each page with a brief summary of key concepts, definitions, and common pitfalls. Then provide deeper explanations.
- **Diagram-first**: Include at least one diagram for complex topics to aid visual understanding.
- **References**: Cite sources at the end with title, author, link, and license when applicable.
- **Worked examples**: Provide small, concrete examples (e.g., code snippets, calculations, diagrams).
- **Tone**: Keep content concise, neutral, and technical. Avoid personal opinions or marketing language.

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

1. **Fork the repository** to your own GitHub account.
2. **Clone your fork** locally: `git clone https://github.com/YOUR_USERNAME/CSKnowledgeHub.git`
3. **Create a feature branch** from `master`: `git checkout -b feature/your-topic-name`
4. **Make your changes** following the content and style guidelines above.
5. **Commit your changes** with clear, descriptive commit messages.
6. **Push to your fork**: `git push origin feature/your-topic-name`
7. **Open a Pull Request** from your fork to the main repository.
   - Reference any related issues (e.g., "Closes #123")
   - Fill in the PR template checklist
   - Ensure your changes pass basic quality checks (markdown formatting, working links)

**Note:** For significant content additions, consider opening an issue first (Content Request) to discuss scope and approach.

## Writing guidelines

- Wrap lines at ~100 characters where reasonable.
- Use lists and tables for scannability; avoid long prose blocks.
- Prefer relative links to repo files; use absolute links for external resources.
- For bilingual content, use clear naming: `README.md` (primary), `README.zh.md` (Chinese), etc.
- Provide alt-text for images to ensure accessibility.

## Licensing

This project is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). By contributing, you agree your contributions will be licensed under the same terms.

## Getting help

Open a Discussion or a Content Request issue if you're unsure about scope or structure.
