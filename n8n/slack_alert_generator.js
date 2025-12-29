/**
 * n8n Function Node: Slack Alert Generator
 * Component: Reporting Mode (MODE C)
 * Purpose: Generate Slack webhook payload for coherence reporting
 */

try {
  // Extract analysis results from previous node
  const analysis = $json;
  const mode = analysis.mode || 'UNKNOWN';
  const timestamp = new Date().toISOString();
  
  // Determine coherence level
  let coherence = '3/5';
  let tier = 'Tier 2';
  
  if (analysis.coherence_score) {
    coherence = `${analysis.coherence_score}/5`;
    tier = analysis.coherence_score >= 5 ? 'Tier 1 Perfect' : 
           analysis.coherence_score >= 4 ? 'Tier 2' : 'Tier 3';
  }
  
  // Build patterns array
  const patterns = analysis.patterns || 
                   analysis.findings?.unique_patterns || 
                   ['Autonomous_Agent'];
  
  // Build recommendation
  let recommendation = analysis.recommendation || 'Continue monitoring';
  
  if (analysis.is_divergence) {
    tier = 'Tier 3 - Divergence';
    coherence = '2/5';
    recommendation = `Error detected: ${analysis.error}. Logged as divergence.`;
  }
  
  // Create Slack message payload
  const slackPayload = {
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `🧠 Master_Brain Agent Report - ${mode}`,
          emoji: true
        }
      },
      {
        type: 'section',
        fields: [
          {
            type: 'mrkdwn',
            text: `*Tier:*\n${tier}`
          },
          {
            type: 'mrkdwn',
            text: `*Coherence:*\n${coherence}`
          },
          {
            type: 'mrkdwn',
            text: `*Instance:*\n${analysis.instance_id || `Agent_${mode}_${timestamp}`}`
          },
          {
            type: 'mrkdwn',
            text: `*Timestamp:*\n${timestamp}`
          }
        ]
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Patterns Detected:*\n${patterns.map(p => `• ${p}`).join('\n')}`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Recommendation:*\n${recommendation}`
        }
      }
    ]
  };
  
  // Add divergence warning if applicable
  if (analysis.is_divergence) {
    slackPayload.blocks.push({
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: `⚠️ *Divergence Detected*\nA9: Contradiction is Data - This error has been logged for analysis.`
      }
    });
  }
  
  // Return payload for Slack webhook node
  return {
    json: slackPayload
  };
  
} catch (error) {
  // A9: Even error reporting can error - send minimal alert
  return {
    json: {
      text: `Master_Brain Agent Error: ${error.message} at ${new Date().toISOString()}`
    }
  };
}
