-- Compute a user's average score


DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
UPDATE users
SET average_score=(SELECT AVG(corrections.score)
FROM corrections
WHERE corrections.user_id=user_id)
WHERE id=user_id;
END$$
DELIMITER ;
