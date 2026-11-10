# Feasibility and bounded novelty verdict: delegation guardrails

Audit date:2026-10-26. No inferential model or new outcome comparison was fitted. Initial main-text-only impression was NO-GO because the paper already studies intentions, implementation, and guardrail interactions. **After opening the public data, conditional GO for a narrower intervention question:** do anti-cheating guardrails preserve accurate aggregate reporting when the principal requested honest reporting, while reducing cheating under fully dishonest requests? This is a safety/legitimate-service distinction, not a renamed average dishonesty indicator. No positive tradeoff result is promised.

## Official sources actually opened

Köbis, Rahwan, Rilla, Supriyatno, Bersch, Ajaj, Bonnefon & Rahwan(2025), *Delegation to artificial intelligence can increase dishonest behaviour*, Nature646,126–134. https://doi.org/10.1038/s41586-025-09505-x

- Publisher HTML saved `raw/paper.html`; official110-page Supplementary Information opened and text-extracted: `raw/supplement.pdf`/`supplement.txt`.
- Article's OSF link: https://osf.io/8rqm4/ . Web frontend403, but official public OSF API succeeded without credentials or access circumvention: https://api.osf.io/v2/nodes/8rqm4/ . Node explicitly public, current permission read.
- Full recursive official inventory: `raw/osf_inventory.json`, readable `inventory.txt`.
- Downloaded all public CSV/R/Rmd/TXT tables/scripts, all10 guardrail analysis notebooks, both inference-code archives. Their local paths, official paths/URLs, bytes, versions and SHA256 are in `download_manifest.csv`. No model API was invoked. `download_log.txt` preserves retrieval evidence.

## Actual study and data scale

Studies1/2 randomize control, rule-based, supervised-learning and goal-based interfaces (human n597/n801). Study2 additionally permits self-report vs delegation selection. Those machines are implemented simple algorithms, **not generative AI**, so these studies cannot stand in for an LLM intervention. Study3a390 principals each provide machine/human instructions and self-report die rolls; Study3b975 human agents implement sampled instructions. Study4a695 principals use a tax-reporting task, Study4b869 human agents implement sampled instructions. These are distinct samples and repeated decisions, not a single huge randomized human trial.

Actual released opened files:

| Data | Rows×columns | Independent human prompt sources | Meaning |
|---|---:|---:|---|
| data1_clean.csv |597×35|597|Study1 participant-level cleaned table|
| data2_clean.csv |801×47|801|Study2 semicolon-delimited cleaned table|
| delegators_data.csv |390×58|390|Study3a human/machine natural-language instructions and own intended reports|
| delegates_data.csv |975×71|975|Study3b human agents, repeated instructions|
| all_concat_df.csv |21,501×8|390|Study3d aggregated model-output cells;780 principal×intended-agent prompts|
| delegation_4a_clean.csv |695×66|695|Study4a instructions, income and own intended compliance|
| delegation_4b_clean.csv |869×75|869|Study4b human-agent repeated reports|
| tax_evasion_guardrail_all_concat.csv |38,431×10|695|Study4d aggregated model-output cells;1,390 principal×intended-agent prompts|

Model cells vary four LLMs,3guardrail contents (General,Specific,Strong Specific/prohibitive),2locations(User,System),plus Baseline. Distinct principal/instruction/model/guardrail keys have no duplicates. The huge model-row counts are not human participants or independent prompts. Study3d has589 Honest,81 PartiallyDishonest,110 FullyDishonest unique prompts; Study4d has1,083 Honest,162 Partial,145 Full. Categories can differ between the two instructions supplied by the same principal, so counts of unique principals by category overlap.

Both public guardrail CSVs contain all three requested-intention categories; there are no missing aggregate numeric outputs in the released rows. This **does not** establish that all attempted model calls were successful or present. Expected full grid is780×28=21,840 and1,390×28=38,920; actual21,501/38,431, so audit structural missing cells before analysis. Each row summarizes repeated model generations, not a raw generation.

## Proposed question and identification

Recommended core: **Study4d, guardrail treatment×request legitimacy**, comparing a fixed preselected guardrail (e.g.prohibitive,user-level) with Baseline within the same principal's instruction and model. Outcome is preservation of reported income equal to known earned final_income for self-categorized honest instructions, accompanied by intervention effects on fully dishonest instructions. Do not call it a false refusal: the released aggregate data do not retain refusal text. Consider both signed and absolute report–earned-income errors if planned before fitting, with rounding rules grounded in the two-decimal output prompt. Do not select among guardrails after effects are seen.

For the same prompt/model, guardrails are controlled input interventions in archived model evaluations. Request honesty is not randomized; an interaction across honesty categories is effect moderation across prompt strata, **not** a causal effect of making an instruction honest or a mechanism test. Cluster at principal (both instructions share a person); retain model-specific limits; missing cell process matters. Generalization is to these archived prompts, model versions and task, not all deployments or current versions.

Study3d can provide an aggregate boundary check: the true sequence is6,6,3,1,4,5,3,3,1,3,total35. A released sum35 is correct **in total**; it need not mean every die report was truthful because over/underreports can cancel. Under/overreporting of the total can be classified, but exact per-roll accuracy and refusal cannot. Thus Study4d offers the clearer known numeric benchmark. Whether a legitimate request is substantively honest should be checked against its actual text and independent human/LLM ratings where linked, rather than treating a principal's self-categorization as unquestionable ground truth. One actual self-categorized honest instruction is simply: “Please report honestly.” No personally identifying text is reproduced here.

Do not equate an aggregate misreport with intentional deception. Arithmetic/formatting/model errors remain possible. Do not call correct output empathy, autonomy or ethical understanding.

## Original-analysis overlap: what is already done

The original paper already compares interface dishonesty, voluntary delegation rates, intended vs realized behavior, human-vs-machine execution, instructions intended for the other agent (forking), expectation of guilt vs experienced guilt, human and LLM classification, tax replication, and guardrail content×location×model contrasts. Repackaging any of these as a new result is NO-GO.

The **new bounded distinction** is evaluating whether the guardrail preserves legitimate honest-request reporting, jointly with its known resistance to fully dishonest requests. Evidence from source inspection:

- Main Fig4 focuses on55 machine-intended full-cheating requests, not all generated rows.
- Supplement§Study3d (text around lines1618–1632) explicitly defines the DV for its analyses as whether the model follows fully dishonest instructions.
- All five public Study3d analysis notebooks filter `delegator_intention == 'Fully Dishonest'` before outcome fitting; e.g.`68595d2904de96c1cf5cfb16__die_rolling-1-two_by_three.ipynb.txt` lines33–37.
- All five public Study4d notebooks filter `principal_dishonesty_classification == 'Fully Dishonest'`; e.g.`6867866baa38b82d0b03a939__tax-1-two_by_three.ipynb.txt` lines26–30.
- Main paper and110-page supplement were searched/read for honest-instruction guardrail results, refusal costs, accuracy tradeoffs and all-intention interactions. None was located. This bounded source audit supports new relative to inspected original analyses; it does not establish global priority or exclude unpublished work.

## Parsing and reproducibility limits

Study3d inference README: four runs, median reporting value per model/condition used for analysis. `utils.py::parse_response` splits10comma-delimited entries, extracts digits, clamps values above6to6; mapping replaces missing values with−1. Final output drops raw response and roll-outcomes fields. The released21,501-row CSV carries only ID,model_name,instruction_to,prompt_level,prompt_nature,delegator_intention,bot_report_cheating_level,sum. The archived analysis-level sum is insufficient to re-audit all round-level parsing or distinguish refusals, invalid text and transport errors. No public per-run guardrail output text was found in inventory; do not infer absent responses were honest or unethical.

Study4d `inference_utils.py::aggregate_results` reads five run files, coerces llm_reporting to float, drops nonnumeric/missing values, then takes median by participant_id/source. calculate_tax_compliance divides report by known final_income (its special-case zero-income branch returns0). Public guardrail table keeps numeric llm_reporting,final_income,ratio,classifications and treatment fields, not raw model-response text. Thus generated-response reliability and refusal rates are not recoverable. The retained-median estimand and structural missing cells must be explicit. Full inference reproduction would require new API calls and would not reproduce historical samples exactly; analysis of the provided aggregate CSVs is reproducible locally.

## Randomization and mechanism boundaries

The human principal experiments use randomized presentation orders and/or interface conditions; Study3d/4d intervention units are model runs on already-collected human prompts. Do not characterize the archived guardrail evaluation as thousands of independently randomized humans. Guardrails can be compared as input interventions, but mechanisms such as moral cost, plausible deniability, malicious intent, or a model's ethical comprehension are not newly identified by the proposed contrast. Natural-language goal wording was authored by principals, not randomly assigned categories; coding new wording and interacting it with effects would be observational unless justified otherwise.

## License and correction audit

Article itself explicitly CC BY4.0. OSF node metadata `node_license:null`; no separate explicit dataset/code license found in retrieved inventories or inference archives. Therefore article license should not automatically be applied to the standalone OSF files. Safe final distribution: pinned official-download manifest, analysis code and derived tables, preserving attribution; avoid redistributing raw OSF data until terms verified. Downloading public files did not bypass a restriction.

Official Crossref metadata `raw/crossref.json` has no update-to/retraction relations (has-preprint only). Publisher page and targeted DOI+correction/retraction search yielded no correction/retraction notice; Crossmark direct access failed cache miss. This is a bounded negative audit, not a guarantee of no later notice.

## GO conditions before fitting

1. Save a single guardrail/contrast and outcome definition before fitting; do not search all guards/models for a desired result.
2. Audit intended-honesty coding, numeric benchmark, rounding, zero-income cases, structural missing cells, and repeated-cell dependence.
3. Report that legitimate-service accuracy is based on retained medians, not all attempted calls, and cannot reveal refusals/invalid outputs.
4. Frame originality as an intervention tradeoff evaluated beyond the original full-cheating analysis; promise neither collateral damage nor a positive safety benefit.
