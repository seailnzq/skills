---
name: policy-to-parents-guide
description: This skill should be used when the user asks to deeply analyze a Chinese government policy document (education, family, youth, technology, employment, etc.) and translate it into practical, actionable guidance for a specific family or personal context such as parents, students, or children. It performs official-source retrieval, core-point extraction, audience-specific impact analysis, and produces a structured markdown report with daily habits and future planning recommendations.
agent_created: true
---

# Policy To Parents Guide

## Overview

This skill turns official Chinese policy documents into concrete, parent-friendly action plans. When a user asks something like “教育部刚发了XX规划，作为家长该怎么理解？” or “这份政策对我家初二孩子有什么影响？”, use this workflow to:
1. Find and verify the official document or authoritative source.
2. Extract the core policy points relevant to the user's audience.
3. Analyze what the policy means for that specific family/person context.
4. Generate a structured markdown report with daily practices and future planning advice.

## Trigger Conditions

Use this skill when the user:
- References a newly issued government policy, plan, guideline, or reform document.
- Asks for a parent-oriented or family-oriented interpretation of policy.
- Wants to apply policy trends to daily education, child development, career planning, or family decisions.

## Workflow

### Step 1: Verify the Document
- Use WebSearch to confirm the policy exists, its official name, issuing body, and release date.
- Prefer sources from gov.cn, state media (Xinhua, CCTV), or central ministry portals.
- If the user’s claim about the document cannot be verified, tell them and ask for clarification rather than inventing content.

### Step 2: Fetch the Full Text
- Use WebFetch on the official source to extract the document contents.
- If the document is too long or WebFetch truncates, fetch the table of contents and key chapters, then use WebSearch to fill gaps.
- Keep a factual summary of the document’s structure and main provisions.

### Step 3: Extract Core Points
- Identify 5–10 policy points that are most relevant to the user’s family context.
- Group them into categories such as: educational goals, curriculum changes, exam/selection reforms, health/mental health, technology/AI, vocational paths, equity, and resource allocation.
- Avoid over-quoting political language; translate official phrasing into plain language for parents.

### Step 4: Analyze Audience Impact
- Ask (or infer from context) the child’s age/grade, family concerns, and location if relevant.
- Connect each policy point to the specific audience:
  - What changes will they face in school?
  - What should the family pay attention to in the next 1–3 years?
  - What risks or opportunities does the policy create?
- Be realistic: distinguish between national policy direction and local implementation timing.

### Step 5: Produce Actionable Guidance
- Create a markdown file in the current workspace with the following sections:
  1. What this policy is and why it matters
  2. Core points (5–10 items)
  3. What it means for the specific family/student context
  4. Daily habits and routines the family can adopt now
  5. Future planning and升学/development path recommendations
  6. Mindset shifts for parents
  7. One-sentence takeaway
- Use relative-path cross-references only if multiple output files are created.
- Present the final file using the present_files tool.

## Tone and Boundaries

- Be helpful, direct, and non-alarmist. Parents are often anxious; provide clarity, not panic.
- Do not invent policy details or make specific predictions about local exam changes unless verified.
- Avoid political commentary. Stick to the document’s stated goals and their practical implications for families.
- When discussing Hong Kong, Taiwan, or Macao, use the standard Chinese formulation: 中国香港 / 中国台湾 / 中国澳门 or Hong Kong, China / Taiwan, China / Macao, China.
- Respect the user’s values while offering evidence-based guidance.

## Output Format

- Primary output: a single markdown report in the workspace root.
- File naming convention: `政策名称_对受众的深度分析与建议.md`
- Example: `教育十五五规划_对初二家长的深度分析与建议.md`

## Notes

- This skill does not require bundled scripts, references, or assets. The example resource directories can be deleted.
- Update this skill if policy interpretation standards change or if the user requests specialized sub-types (e.g., healthcare policy for elderly parents, housing policy for young families).
