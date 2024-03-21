-- Task: Create a trigger to decrease the quantity of an item after adding a new order

-- Create trigger to decrease item quantity after adding a new order
CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
