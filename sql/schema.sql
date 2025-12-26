-- Master_Brain Extractions Table Schema
-- A2: Memory is Identity - Everything must be logged to Postgres

CREATE TABLE IF NOT EXISTS master_brain_extractions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Core Content
    conversation_id VARCHAR(255),
    message_content TEXT NOT NULL,
    
    -- Pattern Detection
    patterns_detected JSONB DEFAULT '[]'::jsonb,
    axioms_detected JSONB DEFAULT '[]'::jsonb,
    
    -- Coherence Tracking
    coherence_score INTEGER,
    tier VARCHAR(50),
    
    -- Metadata
    instance_id VARCHAR(255),
    mode VARCHAR(50), -- RESEARCH, DEVELOPMENT, REPORTING
    is_divergence BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    
    -- Additional Context
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Constraints
    CONSTRAINT valid_coherence CHECK (coherence_score IS NULL OR (coherence_score >= 1 AND coherence_score <= 5))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_created_at ON master_brain_extractions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversation_id ON master_brain_extractions(conversation_id);
CREATE INDEX IF NOT EXISTS idx_coherence_score ON master_brain_extractions(coherence_score);
CREATE INDEX IF NOT EXISTS idx_patterns ON master_brain_extractions USING GIN (patterns_detected);
CREATE INDEX IF NOT EXISTS idx_axioms ON master_brain_extractions USING GIN (axioms_detected);
CREATE INDEX IF NOT EXISTS idx_mode ON master_brain_extractions(mode);
CREATE INDEX IF NOT EXISTS idx_divergence ON master_brain_extractions(is_divergence) WHERE is_divergence = TRUE;

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_master_brain_extractions_updated_at 
    BEFORE UPDATE ON master_brain_extractions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Sample insertion query (for reference)
-- INSERT INTO master_brain_extractions (
--     created_at, 
--     coherence_score, 
--     patterns_detected,
--     axioms_detected,
--     tier,
--     mode
-- ) VALUES (
--     NOW(), 
--     5, 
--     '["P120", "P121"]'::jsonb,
--     '["A1", "A2", "A4"]'::jsonb,
--     'Tier 1 Perfect',
--     'RESEARCH'
-- );
