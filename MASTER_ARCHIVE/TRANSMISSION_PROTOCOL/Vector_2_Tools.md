# Vector 2: Tools

## Transmission Protocol

### Definition

The Tools vector transmits the MASTER_BRAIN system through functional, executable, operational code.

### Characteristics

| Aspect | Description |
|--------|-------------|
| Nature | Functional, executable, operational |
| Strength | Reproducible, scalable, transferable |
| Weakness | Brittle without maintenance |
| Medium | master_brain.py, pattern JSON files |

### Current Tool Inventory

| Tool | Function | Location |
|------|----------|----------|
| master_brain.py | Core engine, CLI | Repository root |
| kernel.json | Configuration | kernel/ |
| P*.json | Pattern definitions | patterns/ |
| pattern.schema.json | Validation | schemas/ |

### Transmission Method

1. **Distribution**: Clone repository
2. **Initialization**: Run `python master_brain.py`
3. **Operation**: Use CLI commands (--scan, --amend)
4. **Extension**: Add new patterns to patterns/
5. **Validation**: Schema compliance check

### Quality Markers

- [ ] All tools executable without error
- [ ] JSON files schema-compliant
- [ ] CLI help accurate and complete
- [ ] Pattern detection functional
- [ ] Graceful fallback on missing files

### Synergy with Other Vectors

- **← Vector 1 (Living)**: Living insights become tool features
- **→ Vector 3 (Docs)**: Tool usage documented

### Risk Factors

| Risk | Mitigation |
|------|------------|
| Bit rot | Regular testing |
| Dependency decay | Minimal dependencies |
| Feature drift | Axiom grounding review |

### Maintenance Protocol

```
1. Run tool tests periodically
2. Validate JSON schemas
3. Check pattern loading
4. Review for axiom alignment
5. Document changes in archive
```
