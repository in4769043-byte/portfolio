# Data card - AI Stack Exchange corpus

## Source
Every question on ai.stackexchange.com that has an accepted answer (data dump, archive.org, 2016-2024).

## Licence
CC BY-SA 4.0 (some posts 3.0). Credit each post by its URL; anything shared from it stays CC BY-SA.

## Records
One JSON line per question: id, title, text, tags, score, created, url.

## Cleaning
HTML stripped, accepted answers only, answer score >= 1, 200-8,000 characters, duplicates removed.

## Known issues
English only; maths formulas left as LaTeX; answers reflect the date they were written.

## Intended use
Retrieval and evaluation in Sessions 09-11 and 21.