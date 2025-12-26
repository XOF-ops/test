/**
 * n8n Function Node: Pattern Analyzer
 * Component: Research Mode (MODE A)
 * Purpose: Analyze patterns from Postgres and detect correlations
 */

try {
  // Get data from Postgres query result
  const extractions = $json.rows || [];
  
  if (extractions.length === 0) {
    return {
      json: {
        status: 'no_data',
        message: 'No extractions found for analysis',
        mode: 'RESEARCH'
      }
    };
  }
  
  // A1: Existence is Relational - Find pattern correlations
  const patternCorrelations = {};
  const axiomPatternMap = {};
  
  extractions.forEach(extraction => {
    const patterns = extraction.patterns_detected || [];
    const axioms = extraction.axioms_detected || [];
    
    // Build pattern co-occurrence matrix
    for (let i = 0; i < patterns.length; i++) {
      for (let j = i + 1; j < patterns.length; j++) {
        const key = `${patterns[i]}::${patterns[j]}`;
        patternCorrelations[key] = (patternCorrelations[key] || 0) + 1;
      }
    }
    
    // Build axiom-pattern correlation
    patterns.forEach(pattern => {
      axioms.forEach(axiom => {
        const key = `${axiom}::${pattern}`;
        axiomPatternMap[key] = (axiomPatternMap[key] || 0) + 1;
      });
    });
  });
  
  // Find strongest correlations
  const topCorrelations = Object.entries(patternCorrelations)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([patterns, count]) => ({
      patterns: patterns.split('::'),
      count: count,
      correlation_strength: count / extractions.length
    }));
  
  const topAxiomPatterns = Object.entries(axiomPatternMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([key, count]) => {
      const [axiom, pattern] = key.split('::');
      return { axiom, pattern, count };
    });
  
  // A4: Process > Results - Document why we found this
  return {
    json: {
      mode: 'RESEARCH',
      analysis_type: 'pattern_correlation',
      timestamp: new Date().toISOString(),
      dataset_size: extractions.length,
      findings: {
        top_pattern_correlations: topCorrelations,
        top_axiom_pattern_correlations: topAxiomPatterns,
        unique_patterns: [...new Set(extractions.flatMap(e => e.patterns_detected || []))],
        unique_axioms: [...new Set(extractions.flatMap(e => e.axioms_detected || []))]
      },
      recommendation: topCorrelations.length > 0 
        ? 'Strong correlations detected - create research report'
        : 'Insufficient data for correlation analysis',
      next_action: 'generate_research_report'
    }
  };
  
} catch (error) {
  // A9: Contradiction is Data
  return {
    json: {
      error: error.message,
      is_divergence: true,
      mode: 'RESEARCH',
      component: 'pattern_analyzer',
      stack: error.stack
    }
  };
}
