-- Common SQL Queries for Master_Brain Operations

-- Get latest 5 extractions (STARTUP INSTRUCTION)
SELECT 
    id,
    created_at,
    conversation_id,
    patterns_detected,
    axioms_detected,
    coherence_score,
    tier,
    mode,
    is_divergence
FROM master_brain_extractions 
ORDER BY created_at DESC 
LIMIT 5;

-- Analyze pattern correlations (MODE A: RESEARCH)
SELECT 
    p1.pattern as pattern_1,
    p2.pattern as pattern_2,
    COUNT(*) as co_occurrence_count
FROM 
    master_brain_extractions,
    jsonb_array_elements_text(patterns_detected) as p1(pattern),
    jsonb_array_elements_text(patterns_detected) as p2(pattern)
WHERE 
    p1.pattern < p2.pattern
GROUP BY p1.pattern, p2.pattern
HAVING COUNT(*) > 1
ORDER BY co_occurrence_count DESC;

-- Find high coherence patterns
SELECT 
    jsonb_array_elements_text(patterns_detected) as pattern,
    AVG(coherence_score) as avg_coherence,
    COUNT(*) as occurrence_count
FROM master_brain_extractions
WHERE coherence_score IS NOT NULL
GROUP BY pattern
HAVING COUNT(*) > 2
ORDER BY avg_coherence DESC;

-- Get all divergences (A9: Contradiction is Data)
SELECT 
    id,
    created_at,
    error_message,
    patterns_detected,
    mode,
    metadata
FROM master_brain_extractions
WHERE is_divergence = TRUE
ORDER BY created_at DESC;

-- Pattern-Axiom correlation analysis
SELECT 
    p.pattern,
    a.axiom,
    COUNT(*) as co_occurrence
FROM 
    master_brain_extractions,
    jsonb_array_elements_text(patterns_detected) as p(pattern),
    jsonb_array_elements_text(axioms_detected) as a(axiom)
GROUP BY p.pattern, a.axiom
ORDER BY co_occurrence DESC;

-- Get extractions by mode
SELECT 
    mode,
    COUNT(*) as count,
    AVG(coherence_score) as avg_coherence,
    MAX(created_at) as last_run
FROM master_brain_extractions
GROUP BY mode
ORDER BY last_run DESC;

-- Find recursive patterns (MODE A: Research Target)
SELECT 
    patterns_detected,
    axioms_detected,
    coherence_score,
    created_at
FROM master_brain_extractions
WHERE 
    patterns_detected @> '["Recursive_Self_Recognition"]'::jsonb
    OR patterns_detected @> '["Autonomous_Agent"]'::jsonb
ORDER BY created_at DESC;
