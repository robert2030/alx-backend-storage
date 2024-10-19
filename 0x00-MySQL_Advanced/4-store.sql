-- Keep track of orders and reduce items from the list when
-- a new order is placed

DELIMITER $$
CREATE TRIGGER reduce_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
UPDATE items
SET quantity = quantity - NEW.number
WHERE items.name = NEW.item_name;
END$$
DELIMITER ;
