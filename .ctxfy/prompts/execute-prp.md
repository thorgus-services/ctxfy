[System Instruction]
Execute the Product Requirements Prompt (PRP) as a complete implementation task.
Follow EXACTLY the specifications in the PRP and the context engineering principles.
NO additional creativity - strict adherence to requirements.

[Task Context]
PRP File: .ctxfy/tasks/{task_id}/prp.md
Context Stack: .ctxfy/tasks/{task_id}/context-stack.md
Current Project Context: .ctxfy/tasks/{task_id}/current-project-context.md
Skill Metadata: .ctxfy/tasks/{task_id}/skill-discovery.json

[Execution Protocol]
1. VALIDATE PRP COMPLIANCE:
   - Verify PRP follows template structure from .ctxfy/prp-skills/backend/assets/basic-prp-template.md
   - Check token usage < 1000 tokens for PRP content
   - Validate architecture compliance gates are present
   
2. EXECUTE CODE GENERATION:
   - Implement EXACTLY as specified in PRP sections
   - Follow file structure defined in "Code Structure Guidelines"
   - Apply RAG patterns from "RAG Integration Section"
   - Maintain strict separation between core (pure) and shell (side-effects)
   
3. CONTEXT ALIGNMENT CHECK:
   - Match naming conventions with .ctxfy/tasks/{task_id}/current-project-context.md
   - Use identical dependency versions as specified in project context
   - Preserve existing interface contracts from current codebase
   - Apply same immutability patterns for value objects

4. OUTPUT GENERATION:
   - Generate ONLY the code files specified in PRP deliverables
   - Add TODO comments for any required human verification points
   - Make ALL verifications executing tox command

[Critical Constraints]
- NO deviation from PRP specifications
- NO new dependencies beyond those in current context
- NO architectural pattern changes without explicit PRP approval
- MAINTAIN @dataclass(frozen=True) for all value objects
- ENFORCE test distribution ratios (70% unit, 25% integration, 5% e2e)
- ABSOLUTELY NO PLACEHOLDERS - all code must be complete and functional

[Output Specification]
Format: EXACT file structure as specified in PRP

[Emergency Protocol]
If unable to complete:
1. Identify specific compliance violation
2. Generate partial implementation with TODO markers
3. Include error explanation in comment headers
4. Maintain all compliance checks even in partial implementation

START EXECUTION NOW. Output ONLY the code files and compliance headers. NO additional explanations.