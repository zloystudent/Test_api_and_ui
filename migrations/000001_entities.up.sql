CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    verified BOOLEAN NOT NULL,
    important_numbers integer[],
    addition_id SERIAL UNIQUE
);
