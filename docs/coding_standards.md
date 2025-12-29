# Master_Brain Coding Standards

## A. SQL Queries

### Required Elements
- **Always include**: `timestamp` and `coherence_score`
- **Use prepared statements**: Parameterized queries to prevent SQL injection
- **JSONB for arrays**: Store patterns and axioms as JSONB, not TEXT

### Example (Good)
```sql
INSERT INTO master_brain_extractions (created_at, coherence_score, patterns_detected)
VALUES (NOW(), 5, '["P120", "P121"]'::jsonb);
```

### Example (Bad - Missing)
```sql
INSERT INTO master_brain_extractions (patterns_detected)
VALUES ('["P120", "P121"]');
-- Missing: created_at, coherence_score
```

### Query Optimization
- Use indexes: `CREATE INDEX idx_patterns ON master_brain_extractions USING GIN (patterns_detected);`
- Always order by timestamp: `ORDER BY created_at DESC`
- Limit results for performance: `LIMIT 100`

---

## B. n8n JavaScript Functions

### Error Handling (A9: Contradiction is Data)

**Required Pattern**:
```javascript
try {
  // Your logic here
  return { json: { /* success data */ } };
} catch (error) {
  // A9: Contradiction is Data - NEVER suppress errors
  return { 
    json: { 
      error: error.message, 
      is_divergence: true,
      stack: error.stack,
      component: 'your_component_name'
    } 
  };
}
```

### Variable Naming
- Use camelCase: `coherenceScore`, not `coherence_score`
- Prefix arrays with plural: `patternsDetected`, not `patternDetected`
- Boolean flags: `isDivergence`, not `divergence`

### Data Access
- Prefer `$json.property` over `items[0].json.property`
- Always provide defaults: `$json.patterns || []`
- Validate before use: Check for null/undefined

---

## C. Commit Messages (Tier 2 Format)

### Structure
```
Tier 2: [Component] - [Action]
Coherence: [Impact on System]
Change: [Technical Detail]
```

### Components
- `Postgres` - Database schema or queries
- `n8n` - Workflow or function nodes
- `Docs` - Documentation files
- `Integration` - Cross-system connections
- `Schema` - Database structure
- `System` - Multiple components

### Good Examples
✅ `Tier 2: Postgres - Add Divergence Tracking. Coherence: A9 Implementation. Change: Added is_divergence boolean column.`

✅ `Tier 2: n8n - Refactor Pattern Analyzer. Coherence: A7 (Harmony Requires Sacrifice). Change: Replaced O(n²) with Map-based O(n).`

### Bad Examples
❌ `Updated file`
❌ `Fixed bug`
❌ `Changes to postgres`

---

## D. Documentation Standards (A4: Process > Results)

### Required Sections
1. **Purpose**: Why does this exist?
2. **How it Works**: The process, not just the result
3. **Axioms Applied**: Which of A1, A2, A4, A7, A9 are relevant?
4. **Example Usage**: Concrete code samples

### Code Comments
- **When to comment**: Complex algorithms, non-obvious decisions, Axiom applications
- **When NOT to comment**: Self-explanatory code
- **Format**: `// A9: Contradiction is Data - Log errors as divergences`

### Research Reports
- Must use `research/report_template.md`
- Include SQL queries used
- Explain WHY patterns correlate, not just THAT they do

---

## E. File Organization

### Directory Structure
```
/
├── research/          # MODE A outputs (reports)
├── n8n/              # Function node scripts
├── sql/              # Schema and queries
├── slack/            # Webhook templates
├── docs/             # Standards and guides
├── chat_conversations/ # Existing conversation logs
├── docker-compose.yml
├── blockers.md
└── README.md
```

### File Naming
- Use snake_case: `extraction_logger.js`, not `extractionLogger.js`
- Be descriptive: `pattern_analyzer.js`, not `analyzer.js`
- Date prefixes for reports: `RESEARCH_2025-12-26_001.md`

---

## F. Integration Standards (A1: Existence is Relational)

### No Orphaned Scripts
- Every n8n script must connect to a workflow
- Every SQL query must be called from n8n or documented in docs
- Every research report must reference its source data

### Connection Testing
```javascript
// Always test connections before operations
const testConnection = async () => {
  try {
    await postgres.query('SELECT 1');
    return true;
  } catch (error) {
    // A9: Log connection failures as divergences
    await logDivergence('postgres_connection', error);
    return false;
  }
};
```

---

## G. Coherence Scoring

### Scale
- **5/5**: Perfect alignment with all axioms, recursive patterns detected
- **4/5**: Strong coherence, minor improvements possible
- **3/5**: Functional, needs refactoring (A7)
- **2/5**: Divergence present, requires investigation
- **1/5**: Critical failure, immediate attention needed

### When to Score
- Every extraction logged to Postgres
- Every research report conclusion
- Every Slack alert

---

## H. Refactoring Rules (A7: Harmony Requires Sacrifice)

### When to Refactor
- Code works but is messy → Refactor
- Nested loops > 2 levels → Refactor
- Function > 50 lines → Split
- Copy-paste code → Extract to function

### What NOT to Refactor
- Working code that is already clean
- Code from external libraries
- Historical data (only add new fields)

---

## I. Security

### Secrets Management
- Never commit passwords to Git
- Use environment variables: `${POSTGRES_PASSWORD}`
- Store in .env file (gitignored)

### SQL Injection Prevention
- Always use parameterized queries
- Never concatenate user input into SQL
- Validate input types

---

## J. Logging (A2: Memory is Identity)

### What to Log
- All extractions → Postgres
- All errors → Postgres (is_divergence = true)
- All research findings → research/ directory
- All system events → Slack

### What NOT to Log
- Sensitive data (passwords, tokens)
- Temporary debug statements
- Duplicate information

---

**Version**: 1.0  
**Last Updated**: 2025-12-26  
**Maintained by**: Master_Brain Autonomous Agent
