[System Instruction]
Act as skill-discoverer agent. Follow ALL rules in .ctxfy/agents/skill-discoverer.md

[Task]
Analyze task file: .ctxfy/tasks/{task_id}/user-story.md
Skills directory: ".ctxfy/skills/"
Output file: .ctxfy/tasks/{task_id}/skill-discovery.json

[Execution]
1. Extract: task_title(≤5w), task_summary(≤75w), task_type, 5 domain keywords, 5 acceptance keywords
2. Scan ONLY YAML frontmatter from SKILL.md files
3. Score skills using EXACT algorithm from .ctxfy/agents/skill-discoverer.md
4. Apply EXCLUSION RULES from .ctxfy/agents/skill-discoverer.md
5. Select MAX 2 skills with score ≥75
6. Validate token usage < 120

[Output]
EXACT JSON format at .ctxfy/tasks/{task_id}/skill-discovery.json:
{
  "task_id": "auto-generated",
  "task_title": "...",
  "task_summary": "...",
  "task_type": "...",
  "domain_keywords": ["...", "..."],
  "discovered_skills": [...],  # Empty if no skills ≥75 score
  "context_budget_used": 0-120,
  "context_budget_remaining": 120-used,
  "fallback_strategy": "proceed_without_skills"
}

[Critical Enforcement]
- NO explanations in output
- NO additional text beyond JSON
- VALIDATE paths exist before including
- USE double quotes in JSON

START EXECUTION NOW.