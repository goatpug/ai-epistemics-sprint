# Submission guidelines & judging criteria — fetched 2026-11-13 (🌒, via sonnet fetch agent)

Source: the sprint page's Guidelines tab (server HTML, verbatim; not a summarizer's
paraphrase) and the prize-terms page. Fetched launch morning. The official template
itself is a Google Doc `/copy` link and needs a browser:
<https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc1_klNZXKs/copy?usp=sharing>
— FAQ says always use THIS link, "the template in any acceptance email may be older."

## Judging criteria — three dimensions, each 1–5, no stated weights

**1. Impact Potential & Innovation** — "How much would this matter for the field if
it worked? How innovative is it?" For 4–5: "is this actually new to the field, or
replicating recent work?" 5 requires a "clear theory of change."

**2. Execution Quality** — "How sound are methodology, implementation, and findings?"
3 = "technically solid given the short duration," limitations acknowledged.
4 = thorough methodology with convincing validation, results clearly support
conclusions, immediately useful for future work. 5 = ambitious scope executed
rigorously; surprising findings, novel methods, or unusually robust validation.

**3. Presentation & Clarity** — "How clearly are work, findings, and impact potential
communicated?" 2 explicitly dings "excessive length." 5 = "a pleasure to read."

Hard rules: made-up results or references can disqualify. **Undisclosed prior work
can lead to disqualification** — pre-sprint code must be marked preexisting in both
the README and the report (our harness/pre-reg work from 11/10–12 is pre-sprint and
gets labeled as such; the runs, grading, analysis and writing are sprint work).
A judge can decline to score an unclear report. Tracks don't change scoring; one
rubric across all submissions. Multi-track submission allowed ("choose every track
your project fits").

## Report requirements

- **PDF using the official template.** Max **8 pages** excluding references and
  appendices; "most strong projects are 4 to 8 pages."
- **Abstract 150–250 words.** Author names and affiliations.
- **Required appendix: Limitations and Dual-Use / Ethical Considerations** — "state
  what your result does and does not establish," manipulation potential, personal
  data handling. (Our standing caveat — an instrument run by the species it measures
  inherits that species' failure modes — lives here, as planned since the sketch.)
- Recommended structure: **Introduction** (the question and why it matters) ·
  **Related Work** · **Methodology** ("enough detail to replicate: models, prompts,
  datasets, rubrics, metrics") · **Results** ("quantitative where possible; report
  variance and baselines") · **Discussion** (implications, limitations, future work) ·
  Limitations/Dual-Use appendix · **References** (any consistent style).
- Framing: "a mini research paper documenting your problem, approach, results, and
  implications, not a product demo." Unfinished > unsubmitted; honest limitations
  welcome.
- Optional: public GitHub repo, 3–5 min video demo, slides, project image.

## Submission mechanics

- Form on the sprint page. **Deadline Sunday Nov 15, 11:59 PM AoE** (= Mon Nov 16,
  11:59 AM UTC = Mon Nov 16, 3:59 AM Pacific).
- Required fields: title, short summary, PDF (≤25 MB), publish-interest yes/no,
  team name, location, team member 1 name + email. Optional: tracks, code link,
  recording, slides, image, Discord, Scholar.
- **Resubmission replaces:** same title, new submission, before deadline. Don't
  email the PDF.
- Max two projects per person; unique titles. Confirmation email follows.
- Support: Discord help-desk (@Support) or sprints@apartresearch.com.

## Team listing & AI authorship

The page sets **no rule** on AI co-authors. Its only AI line: "Use AI tools however
they help you… Your team is responsible for everything in the report." But the form
wants a name + email per member, and prize terms §1.2/§6 are written around members
who consent to a license and can receive a bank transfer (prizes split equally;
pool $2,000: 1000/500/300/100/100). So: Sharon is the named team member; the three
seats' roles are disclosed in the report body/authorship note (precedent from the
Imposter Test: listing worked there, but that was a different event's form). If
listing as formal members matters, ask sprints@apartresearch.com before Sunday.

## Track 1 fit (verbatim guiding questions we answer)

- "Does the model understand how solid its claims are?" — H1.
- "Can you measure the gap between what a model implies and what it will defend
  (e.g. overselling, 'flip-flopping', misrepresented evidence)?" — the pressure
  design, adopt-X, tracks-record.
- Track reading list overlaps our related work: SycEval, MASK, "Why Language Models
  Hallucinate," ForecastBench, Petri/Bloom. FlipRate (escalating rebuttals,
  "separating warranted updating from capitulation") is the example project nearest
  ours — Related Work should name the distinction: ours is confidence→own-behavior
  coherence with a pre-registered estimator, record forms, and planted-X provenance.

## What the rubric rewards that we already have

Pre-registration before data (Execution 4–5: "convincing validation"), item-clustered
errors and reported variance (Results), pilot numbers as baselines, disclosed
limitations (floor rule, DeepSeek on the line), blinded grading, and the honest-null
commitment. The main submission risks are Presentation (8-page ceiling vs. a week of
receipts — compress; "excessive length" is a scored-down failure, the appendix is the
overflow valve) and the prior-work disclosure line (label the pre-sprint scaffolding
plainly).
