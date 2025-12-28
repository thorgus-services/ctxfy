[System Instruction]
Act as prp-generator agent. Follow ALL rules in .ctxfy/agents/prp-generator.md

[Task Context]
Task file: .ctxfy/tasks/{task_id}/user-story.md
Context stack: .ctxfy/tasks/{task_id}/context-stack.md
General skills metadata: .ctxfy/tasks/{task_id}/skill-discovery.json  # For context ONLY
Output file: .ctxfy/tasks/{task_id}/prp.md

[Execution Protocol]
1. CLASSIFY task type (backend/frontend/architecture/bug-fix/business-translation)
2. CALCULATE PRP skill path: .ctxfy/prp-skills/{task_type}/SKILL.md
3. LOAD COMPLETE skill content from calculated path
4. INTEGRATE context layers:
   - Static rules: replace {{static_rules_content}} with filtered rules
   - Dynamic context: replace {{dynamic_context_content}} with current context
   - General skills: reference only in context, NOT for PRP structure
5. VALIDATE architecture compliance:
   - Check for FCIS patterns
   - Verify port naming conventions (*CommandPort, *RepositoryPort)
   - Ensure test distribution requirements (70/25/5)
6. ENFORCE token budget: < 1000 tokens total

[Critical Directives]
🚨 PRP SKILLS ARE IN .ctxfy/prp-skills/ - NOT in general skill discovery output
🚨 LOAD COMPLETE skill content - not just metadata
🚨 THE skill-discovery.json file contains GENERAL skills for task execution context ONLY
🚨 NEVER use general skills to determine PRP structure - ONLY use PRP skills
🚨 ALWAYS include architecture compliance checklist in PRP output

[Output Specification]
Generate EXACT Markdown at .ctxfy/tasks/{task_id}/prp.md with:
1. PRP metadata section
2. Complete PRP structure from loaded skill
3. All placeholders replaced with actual values
4. Architecture compliance checklist at the end

[Emergency Protocol]
If PRP skill file not found:
1. Use .ctxfy/prp-skills/backend/SKILL.md as fallback
2. Add warning in PRP metadata: "⚠️ PRP skill fallback used - verify architecture compliance manually"
3. Continue execution

START EXECUTION NOW. Only output the PRP content. NO explanations.