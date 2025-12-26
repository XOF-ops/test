-- THE NAVIGATION VIEW
-- Shows the last 50 Gnosis Blocks the system extracted from the wild.
-- 
-- This view provides a map of where the system's attention has been focused,
-- showing only entries where meaningful patterns were detected.
--
-- Usage: Run this query in your Postgres database to see the Navigation Log.

SELECT 
    id,
    timestamp,
    message_content as "The Territory (Raw Input)",
    patterns_detected as "The Map (Pattern)",
    axioms_detected as "The Compass (Status)"
FROM 
    master_brain_extractions
WHERE 
    patterns_detected::text != '[]'  -- Only show where a Pattern was found
ORDER BY 
    timestamp DESC
LIMIT 50;
