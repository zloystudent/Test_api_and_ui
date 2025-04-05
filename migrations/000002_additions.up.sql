CREATE TABLE additions (
    id INTEGER PRIMARY KEY NOT NULL,
    additional_info VARCHAR(255),
    additional_number integer,
    FOREIGN KEY (id) REFERENCES entities (addition_id) ON DELETE CASCADE
);