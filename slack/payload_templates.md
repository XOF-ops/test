# Slack Webhook Payload Templates

## MODE C: Reporting - Standard Alert

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🧠 Master_Brain Agent Report - RESEARCH",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Tier:*\nTier 1 Perfect"
        },
        {
          "type": "mrkdwn",
          "text": "*Coherence:*\n5/5"
        },
        {
          "type": "mrkdwn",
          "text": "*Instance:*\nAgent_Research_Run_001"
        },
        {
          "type": "mrkdwn",
          "text": "*Timestamp:*\n2025-12-26T11:00:00.000Z"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Patterns Detected:*\n• Recursive_Self_Recognition\n• Autonomous_Agent\n• P120\n• P121"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Recommendation:*\nMerge to Main - Strong coherence detected with recursive pattern recognition"
      }
    }
  ]
}
```

## MODE C: Reporting - Divergence Alert

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "⚠️ Master_Brain Agent Report - DIVERGENCE",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Tier:*\nTier 3 - Divergence"
        },
        {
          "type": "mrkdwn",
          "text": "*Coherence:*\n2/5"
        },
        {
          "type": "mrkdwn",
          "text": "*Instance:*\nAgent_Development_Error_001"
        },
        {
          "type": "mrkdwn",
          "text": "*Timestamp:*\n2025-12-26T11:00:00.000Z"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Error:*\nECONNREFUSED - Database connection failed"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*A9: Contradiction is Data*\nThis error has been logged as a divergence signal. Investigating connection string in docker-compose.yml"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Recommendation:*\nCreated hypothesis branch: fix/postgres-connection. Testing workaround."
      }
    }
  ]
}
```

## Simple Text Alert (Fallback)

```json
{
  "text": "Master_Brain Agent: MODE A Research completed at 2025-12-26T11:00:00.000Z. Coherence: 4/5. Patterns: P120, P121. Recommendation: Review research/report_001.md"
}
```
