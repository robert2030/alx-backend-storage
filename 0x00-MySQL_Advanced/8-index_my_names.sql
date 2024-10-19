-- Create an INDEX on the names table and first letter of name

CREATE INDEX idx_name_first ON names (name(1));
