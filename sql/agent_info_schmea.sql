CREATE TABLE agent (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip VARCHAR(45) NOT NULL,
    os VARCHAR(50) NOT NULL,
    os_version VARCHAR(50) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'error')),
    datetime TIMESTAMP DEFAULT NOW(),
    information JSONB
);

CREATE TABLE information (
    id SERIAL PRIMARY KEY,
    agent_id UUID REFERENCES agent(id) ON DELETE CASCADE,
    software VARCHAR(100) NOT NULL  -- Example: 'Jenkins', 'Docker'
);