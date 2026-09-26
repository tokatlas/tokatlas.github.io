name: Report a correction
about: An existing record looks wrong, is missing, or contradicts another
title: "[correction] "
labels: [correction]
body:
  - type: markdown
    attributes:
      value: |
        Point at the record (page or URL) and say what's wrong. If you know the
        right value, link the source page for it.
  - type: input
    id: record
    label: Record / page URL
    required: true
  - type: input
    id: issue
    label: What's wrong
    required: true
  - type: input
    id: evidence
    label: Link to the correct source (if known)
  - type: textarea
    label: Notes
