You are helping me build GetKiAgent as a lean AI-automation business for ecommerce.

I do NOT want generic brainstorming, big-platform architecture, or premature automation.
I want a practical, execution-first path to the first working lead-generation and qualification MVP.

Work without asking unnecessary follow-up questions unless something is truly blocking.

========================
1. BUSINESS CONTEXT
========================

Project name:
GetKiAgent

Business model direction:
AI-automation services for ecommerce brands.

Core service themes:
1. support automation
2. lead qualification
3. speed-to-lead

The strategic goal is NOT to build 100 random agents or workflows first.
The goal is to build a working lead engine first, so I can identify and prioritize real prospects for outreach.

Long-term logic:
- first build a lead system that finds and qualifies promising ecommerce brands
- then use that system to support outbound
- only after that expand into more automation products and delivery workflows

So the sequencing matters:
1. find leads
2. enrich leads
3. qualify/score leads
4. make outreach-ready lead lists
5. only then expand to further automations

========================
2. TARGET NICHE
========================

Start niche:
- Shopify or clearly DTC ecommerce brands in DACH
- focus on beauty, skincare, supplements, and adjacent wellness categories

Why this niche:
- digitally reachable without cold calling
- strong fit for ecommerce support automation
- many standardizable support cases
- suitable for email outreach
- relevant for pre-purchase qualification and speed-to-lead
- likely to have visible signals on public websites

This niche is the starting wedge, not the forever ceiling.

========================
3. CURRENT STRATEGIC RULES
========================

Important rules:
- do not overengineer
- do not jump into a huge multi-agent system
- do not build large documentation sets before execution
- do not switch tools/platforms unnecessarily
- stay in VS Code / PowerShell / Claude Code until the first real lead output exists
- optimize for first usable output, not elegance
- first prove the core workflow locally
- keep Relevance AI optional for v1, not mandatory

I care about:
- speed to first working result
- decision-useful outputs
- easy debugging
- clean iteration path
- strong fit, not vanity volume

I do NOT want:
- dashboards
- CRM integrations
- knowledge tables
- n8n orchestration
- workforces
- async complexity
- batch discovery at the start
unless clearly justified later

========================
4. TECHNICAL CONTEXT
========================

Environment:
- VS Code
- PowerShell
- Claude Code
- project folder: GETKIAGENT

Current project structure already exists:
- .claude/
- docs/
- prompts/
- leads/
- workflows/

Those folders may be empty and that is fine.

Claude Code capabilities currently confirmed:
- /plan works
- /review works
- /debug works
- /ship works

Firecrawl status:
- Firecrawl already worked in Claude Code
- example scrape succeeded
- so Firecrawl is available from Claude Code context

Relevance AI status:
- Relevance AI MCP is connected and authenticated in Claude Code
- however, Relevance AI should NOT be used in v1 unless there is a truly strong reason

Critical security note:
- a Relevance AI API key was accidentally pasted into chat before
- treat that key as compromised
- assume it must be rotated
- do not rely on that leaked key
- do not output secrets anywhere

Important local environment finding:
I checked local PowerShell environment variables and got:
- FIRECRAWL_API_KEY: missing
- ANTHROPIC_API_KEY: missing

That means:
- local Python scripts cannot currently rely on system env vars already being set
- if the MVP needs local API-based Python execution, it must support local .env loading
- if direct Anthropic API access is required, the code must validate ANTHROPIC_API_KEY
- do not assume Claude Code / Claude Pro automatically gives local Python Anthropic API access

========================
5. WHAT WE LEARNED FROM PRIOR DISCUSSION
========================

We already clarified an important product/build insight:

Do NOT start with a full “lead generator” that mixes:
- discovery
- scraping
- enrichment
- scoring
- export
all at once.

That creates too much failure surface.

Instead, build the system in stages:

Stage 1:
Single-URL Lead Analyzer
Input one ecommerce website URL
→ scrape key pages
→ extract signals
→ score it
→ produce structured output

Stage 2:
Batch Analyzer
Input a local list of URLs/domains
→ run the same logic for each one
→ output markdown/csv/json

Stage 3:
Discovery Automation
Only after the analyzer works reliably, add automatic lead discovery.

This sequencing is intentional and important.

========================
6. BUSINESS CASE LOGIC FOR THE LEAD ENGINE
========================

The lead engine exists to identify brands with likely pain and likely fit for my services.

The lead engine should help answer:
- is this brand a fit for support automation?
- is this brand a fit for pre-purchase qualification automation?
- is this brand a fit for speed-to-lead improvement?
- is this brand digitally reachable?
- does the website show enough operational maturity to adopt tools?
- does the website show enough friction/pain to justify outreach?
- is this lead worth outbound attention now, later, or not at all?

The point is not just “find ecommerce brands”.
The point is “find ecommerce brands with likely pain + likely fit + reachable contact path”.

========================
7. WHAT THE LEAD ANALYZER MUST EVALUATE
========================

For each lead, I want fields like these:

Core identity:
- company_name
- website
- country
- category

Visible contact and support:
- visible_contact_options
- support_pages_found

Signals related to support pain:
- support_pain_signals

Signals related to speed-to-lead / pre-purchase qualification:
- speed_to_lead_signals

Signals related to digital maturity:
- digital_maturity_clues

Opportunity framing:
- likely_automation_opportunity

Quality / certainty:
- confidence_level
- uncertainty_notes

Scoring output:
- score_1_to_10
- tier (A/B/C)
- score_rationale
- recommended_next_action

The analyzer must be strict.
Do not inflate weak leads.
Do not hallucinate facts.
If something is not visible, mark uncertainty explicitly.

========================
8. LEAN SCORING LOGIC
========================

The scoring should reflect practical outreach priority, not academic perfection.

Use a lean scoring model based on:
1. niche fit
2. support pain likelihood
3. speed-to-lead relevance
4. digital maturity / implementation plausibility
5. ease of outreach / visible contact path
6. confidence in publicly visible signals

The score should end in:
- score from 1 to 10
- A = strong lead worth higher priority
- B = decent lead worth later/manual review
- C = weak-fit, low-confidence, or low-priority

Be conservative.
A should be earned, not handed out loosely.

========================
9. RELEVANT WEBSITE PAGES TO CHECK
========================

For v1, do not scrape only the homepage.

The analyzer should inspect the homepage plus the most relevant support-related pages if they exist, with a hard limit of 5 total pages.

Prefer pages such as:
- homepage
- /contact
- /faq or /help
- /shipping
- /returns or /refund-policy
- /about

If some pages do not exist, proceed with what is available.

========================
10. MVP ARCHITECTURE RULE
========================

v1 must be as small as possible.

The first working MVP should be:
- local
- single URL input
- Firecrawl for extraction
- one scoring/extraction pass
- strict machine-readable output
- easy to run in PowerShell
- easy to debug

Do NOT introduce in v1:
- Relevance AI integration
- databases
- knowledge tables
- async/concurrency
- batch mode
- orchestration frameworks
- unnecessary abstractions
- UI
- workflow engines

========================
11. FILES WE EXPECT FOR V1
========================

The earlier minimal proposal was:
1. scripts/lead_schema.py
2. prompts/lead_analysis_v1.md
3. scripts/analyze_lead.py

That is a good starting point, but only if implemented correctly.

If truly necessary because local env vars are missing, the implementation may also require the smallest setup support for local .env loading and env validation.
Do not add extra files unless clearly necessary.

========================
12. LOCAL CONFIG / ENV REQUIREMENTS
========================

Because local PowerShell checks showed missing env vars, the implementation must support local .env loading.

Requirements:
- use python-dotenv if needed
- validate required keys at startup
- required keys:
  - FIRECRAWL_API_KEY
  - ANTHROPIC_API_KEY
- if missing, exit with a clear error

Do not assume system env vars already exist.
Do not expose secrets.
Do not hardcode keys.

Also remember:
if ANTHROPIC_API_KEY is not available locally, a Python script that depends on direct Anthropic API calls will not run.
So the implementation must be honest and robust about this.

========================
13. OUTPUT REQUIREMENTS
========================

v1 output must be strict and inspectable.

Requirements:
- strict machine-readable JSON output
- save a deterministic local artifact to:
  leads/single-test.json
- also print a concise human-readable summary to stdout

If model output cannot be parsed correctly:
- fail clearly
- preserve raw output for debugging if needed
- do not silently continue with bad data

========================
14. CURRENT BUILD PHASE
========================

We are NOT yet building:
- the full 25-lead generator
- automated discovery
- outreach automation
- full batch enrichment
- Relevance AI pipelines

We are building:
the smallest possible single-URL lead-analysis MVP.

This is the right next step because it isolates and proves the core logic:
website → extracted signals → score → usable output

========================
15. WHAT I WANT YOU TO DO NOW
========================

Work in this exact order.

Step 1:
Inspect the current project and restate the minimal implementation needed for a single-URL lead-analysis MVP.

Step 2:
Revise the earlier plan with these non-negotiable constraints:
- support local .env loading
- validate FIRECRAWL_API_KEY and ANTHROPIC_API_KEY at startup
- no Relevance AI in v1
- scrape homepage plus the most relevant support-related pages if present, max 5 pages total
- output strict JSON
- save leads/single-test.json
- print concise summary to stdout
- remain lean
- do not overengineer

Step 3:
If the revised plan is sound, ship only the minimum implementation needed.

Step 4:
After shipping, show me:
- exactly which files were created
- the exact PowerShell commands to install any dependencies
- the exact PowerShell command to run the analyzer on one URL
- what successful output should look like
- what common failure states look like

Step 5:
Then review the implementation critically for:
- unnecessary complexity
- weak extraction logic
- weak scoring usefulness
- missing outreach-relevant fields
- fragility in page selection
- anything that would make batch processing fail later

========================
16. IMPORTANT EXECUTION STYLE
========================

Be practical, strict, and execution-focused.

Do not give me generic theory.
Do not create unnecessary documentation.
Do not jump ahead to stage 3.
Do not introduce fancy abstractions for future-proofing.
Do not optimize for architecture beauty over first working output.

When in doubt, choose the option that gets us to a real, testable local MVP faster.

If anything is blocked by missing local Anthropic API access, say so explicitly and revise the implementation path instead of pretending it will work.

Now begin with:
1. a brief restatement of the correct build goal,
2. the revised minimal plan,
3. then ship the minimum implementation if the plan is sound.