/**
 * n8n Function Node: Master_Brain Extraction Logger
 * Component: Memory System (A2: Memory is Identity)
 * Purpose: Log extraction data to Postgres with proper error handling
 */

// A9: Contradiction is Data - Always handle errors
try {
  // Extract data from previous node
  const conversationId = $json.conversation_id || $json.id;
  const messageContent = $json.message_content || $json.content;
  const patternsDetected = $json.patterns_detected || [];
  const axiomsDetected = $json.axioms_detected || [];
  const coherenceScore = $json.coherence_score || null;
  const tier = $json.tier || null;
  const mode = $json.mode || 'DEVELOPMENT';
  
  // Prepare SQL query
  const sql = `
    INSERT INTO master_brain_extractions (
      created_at,
      conversation_id,
      message_content,
      patterns_detected,
      axioms_detected,
      coherence_score,
      tier,
      mode,
      instance_id,
      metadata
    ) VALUES (
      NOW(),
      $1,
      $2,
      $3::jsonb,
      $4::jsonb,
      $5,
      $6,
      $7,
      $8,
      $9::jsonb
    ) RETURNING id, created_at;
  `;
  
  const params = [
    conversationId,
    messageContent,
    JSON.stringify(patternsDetected),
    JSON.stringify(axiomsDetected),
    coherenceScore,
    tier,
    mode,
    `Agent_${mode}_${new Date().toISOString()}`,
    JSON.stringify($json.metadata || {})
  ];
  
  // Return for Postgres node
  return {
    json: {
      sql: sql,
      params: params,
      operation: 'insert_extraction'
    }
  };
  
} catch (error) {
  // A9: Contradiction is Data - Log the error as a divergence
  return {
    json: {
      error: error.message,
      is_divergence: true,
      stack: error.stack,
      original_data: $json,
      mode: 'ERROR_CAPTURE'
    }
  };
}
