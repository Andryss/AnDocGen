# Документация AnDocGen: аналитический обзор

Каталог `docs/preliminary_report/` содержит материалы раннего исторического отчёта по теме «Обзор предметной области тематики выпускной квалификационной работы».

**Дата отчёта:** 21.01.2026.

Документы соответствуют этапам [индивидуального задания](individual_assignment.md) и оформлены в Markdown для конвертации в DOCX через Pandoc.

## Соответствие этапам задания

| Этап | Документ | Содержание |
|------|----------|------------|
| 3 | [sources.md](sources.md) | Список источников для аналитического обзора, библиографические описания, ссылки и даты обращения |
| 4 | [literature_review.md](literature_review.md) | Введение в предметную область, таксономия и сравнение подходов, критический анализ, обоснование актуальности, перспективные направления, выводы и библиография |

## Рекомендуемый порядок чтения

1. [individual_assignment.md](individual_assignment.md) — тема и рабочий план-график.
2. [sources.md](sources.md) — список источников для аналитического обзора.
3. [literature_review.md](literature_review.md) — аналитический обзор с таблицами, классификационной схемой и списком использованных источников.

## Конвертация в DOCX

Команды выполняются из корня репозитория:

```bash
pandoc docs/preliminary_report/individual_assignment.md -o individual_assignment.docx
pandoc docs/preliminary_report/sources.md -o sources.docx
pandoc docs/preliminary_report/literature_review.md --resource-path=docs/preliminary_report -o literature_review.docx
```

## Связанные материалы в репозитории

- [Общий указатель документации](../README.md)
- [README проекта](../../README.md)
