# Contributing to CSKnowledgeHub

Thank you for helping improve this knowledge hub. This guide covers content guidelines and contribution workflow.

## Scope

**In scope:** computer systems, programming foundations, data structures, algorithms, study resources with annotations, and runnable Labs.

**Out of scope:** problem dumps, proprietary content, framework tutorials, and unrelated DevOps guides.

## Content Guidelines

- Start with a brief summary, then provide detailed explanations.
- Include diagrams for complex topics.
- Provide concrete examples, experiments, or calculations where useful.
- Use a professional, technical tone.
- Cite sources at the end.
- Use `#` for the title and `##` for sections.
- Include a table of contents for long pages.
- Use lowercase kebab-case for ordered Markdown files and directories, for example `01-process-and-threads.md`.
- Keep language-specific source file names idiomatic, such as `main.py`, `main.go`, and `test_main.py`.

## Adding New Topics

1. Add course notes under `courses/` or foundation notes under `foundations/`.
2. Keep chapter files in the relevant directory and use a numeric prefix when order matters.
3. Add small, focused examples with the relevant course material.
4. Add larger implementations under `labs/` with language directories such as `python/` and `go/`.
5. Update the nearest existing README when the public index changes.

## How to Contribute

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-topic`.
3. Make your changes following these guidelines.
4. Commit with a clear message.
5. Push and open a Pull Request.

For major changes, open an Issue first to discuss the scope.

## License

By contributing, you agree that your contributions will be licensed as follows:

- **Documentation and notes:** [CC BY 4.0](LICENSE)
- **Code examples:** [MIT License](LICENSE-CODE)
