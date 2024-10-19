-- Lists all students who need meeting and meet the requirement
-- Have no last meeting date or last meeting date is less than 1 month

CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80 AND (last_meeting IS NULL OR last_meeting < ADDDATE(CURDATE(), INTERVAL -1 MONTH));
