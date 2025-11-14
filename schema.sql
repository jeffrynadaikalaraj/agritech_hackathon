-- AgriFlow PostgreSQL Schema
-- Optional: Use this for production PostgreSQL setup

CREATE TABLE farmers (
    id SERIAL PRIMARY KEY,
    farmer_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    district VARCHAR(100),
    land_size_ha FLOAT,
    soil_health JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    farmer_id VARCHAR(50) NOT NULL REFERENCES farmers(farmer_id),
    dcs_score FLOAT,
    ndvi_score FLOAT,
    risk_level VARCHAR(20),
    recommended_amount FLOAT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    farmer_id VARCHAR(50) NOT NULL,
    upi_id VARCHAR(100),
    amount FLOAT,
    status VARCHAR(20) DEFAULT 'PENDING',
    razorpay_id VARCHAR(100),
    triggered_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE whatsapp_logs (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    message_in TEXT,
    message_out TEXT,
    interaction_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_farmer_id ON farmers(farmer_id);
CREATE INDEX idx_farmer_phone ON farmers(phone);
CREATE INDEX idx_assessment_farmer ON assessments(farmer_id);
CREATE INDEX idx_transaction_farmer ON transactions(farmer_id);
CREATE INDEX idx_transaction_status ON transactions(status);
CREATE INDEX idx_whatsapp_phone ON whatsapp_logs(phone);
