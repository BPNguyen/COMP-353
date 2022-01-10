/* Lab 2 */

-- Use appropriate DB
-- USE Big_Pine_Valley
-- USE Pine_Valley

-- Cross product (w/o JOIN clause)
SELECT * 
FROM Customer_T, Order_T;

-- Cross product (w JOIN clause)
SELECT *
FROM Customer_T
JOIN Order_T;

-- Inner join (w/ WHERE clause)
SELECT C.CustomerID, O.CustomerID, C.CustomerName, O.OrderID
FROM Customer_T as C, Order_T as O
WHERE C.CustomerID = O.CustomerID
ORDER BY O.OrderID;

-- Inner join (w/ JOIN clause)
SELECT C.CustomerID, O.CustomerID, C.CustomerName, O.OrderID m
FROM Customer_T as C 
JOIN Order_T as O 
	USING (CustomerID)
ORDER BY O.OrderID;

-- Natural join (EQUI JOIN in which cols. w/ same name appear only once)
SELECT *
FROM Customer_T as C
NATURAL JOIN Order_T as O
ORDER BY O.OrderID;

-- Left outer join
SELECT C.CustomerID, C.CustomerName, O.OrderID
FROM Customer_T as C
LEFT OUTER JOIN Order_T as O
	USING (CustomerID)
ORDER BY O.OrderID;

-- Right outer join
SELECT C.CustomerID, C.CustomerName, O.OrderID
FROM Customer_T as C
RIGHT OUTER JOIN Order_T as O
	USING (CustomerID)
ORDER BY O.OrderID;

-- Assemble all information necessary to create an invoice for Order 1006
-- USE Pine_Valley
SELECT O.OrderID as InvoiceNo, O.OrderDate, C.CustomerName, C.CustomerAddress, C.CustomerCity, C.CustomerState, C.CustomerPostalCode, OL.OrderedQuantity, P.ProductDescription, P.ProductStandardPrice, (OL.OrderedQuantity * P.ProductStandardPrice) AS Amount
FROM Order_T as O, Customer_T as C, OrderLine_T as OL, Product_T as P
WHERE O.CustomerID = C.CustomerID
	AND O.OrderID = OL.OrderID
     AND OL.ProductID = P.ProductID
	AND O.OrderID = 1006;
    
-- Self join (typically for Unary relationships)
-- USE Pine_Valley
-- USE Big_Pine_Valley
SELECT E.EmployeeID, E.EmployeeName, M.EmployeeName as Manager
FROM Employee_T as E, Employee_T as M
WHERE E.EmployeeSupervisor = M.EmployeeID;

-- Select name and address of customer placing Order 1008
-- USE Pine_Valley
SELECT C.CustomerName, C.CustomerAddress, C.CustomerCity, C.CustomerState, C.CustomerPostalCode
FROM Customer_T as C, Order_T as O
WHERE C.CustomerID = O.CustomerID
	AND O.OrderID = 1008;

-- Above as subquery
-- USE Pine_Valley
SELECT C.CustomerName, C.CustomerAddress, C.CustomerCity, C.CustomerState, C.CustomerPostalCode
FROM Customer_T as C
WHERE C.CustomerID = 
	(SELECT O.CustomerID
     FROM Order_T as O
     WHERE O.OrderID = 1008);
     
-- Names of customers who've placed orders?
-- USE Big_Pine_Valley
SELECT C.CustomerName
FROM Customer_T as C
WHERE C.CustomerID IN 
	(SELECT DISTINCT O.CustomerID
     FROM Order_T as O);
     
-- Which customers haven't placed orders for Computer Desks?
-- USE Big_Pine_Valley
SELECT C.CustomerID, C.CustomerName
FROM Customer_T as C
WHERE C.CustomerID NOT IN 
	(SELECT O.CustomerID
     FROM Order_T as O, OrderLine_T as OL, Product_T as P
     WHERE O.OrderID = OL.OrderID
     	AND OL.ProductID = P.ProductID
     	AND P.ProductDescription = 'Computer Desk');
        
-- Correlated subquery
-- What are the OrderIDs for all orders that have included Natural Ash-finished furniture?
-- USE Pine_Valley
SELECT DISTINCT OL.OrderID
FROM OrderLine_T as OL
WHERE EXISTS 
	(SELECT *
     FROM Product_T as P
     WHERE P.ProductID = OL.ProductID
     	AND P.ProductFinish = 'Natural Ash');
        
-- List details about product with highest standard price
SELECT PA.ProductID, PA.ProductDescription, PA.ProductFinish, PA.ProductStandardPrice
FROM Product_T as PA
WHERE PA.ProductStandardPrice > ALL 
	(SELECT PB.ProductStandardPrice
     FROM Product_T as PB
     WHERE PB.ProductID != PA.ProductID);

-- Derived tables
-- Show desc, standard price, and overall average standard price for all products with a standard price higher than the average standard price
SELECT P.ProductDescription, P.ProductStandardPrice, ProductAvg.AvgPrice
FROM 
	(SELECT AVG(ProductStandardPrice) AS AvgPrice
     FROM Product_T) AS ProductAvg, Product_T AS P
WHERE P.ProductStandardPrice > ProductAvg.AvgPrice;

-- Union
-- Show customer(s) who've, in a given line item, puchased the largest quantity of any product and customer(s) who've, in a given line item, purchased the smallest quantity, returning the result in one table
SELECT C1.CustomerID, C1.CustomerName, OL1.OrderedQuantity, 'Largest Quantity' AS Quantity
FROM Customer_T C1, Order_T O1, OrderLine_T OL1
WHERE C1.CustomerID = O1.CustomerID
	AND O1.OrderID = OL1.OrderID
    AND OL1.OrderedQuantity = 
    	(SELECT MAX(OL.OrderedQuantity)
         FROM OrderLine_T OL)
UNION
SELECT C2.CustomerID, C2.CustomerName, OL2.OrderedQuantity, 'Smallest Quantity' AS Quantity
FROM Customer_T C2, Order_T O2, OrderLine_T OL2
WHERE C2.CustomerID = O2.CustomerID
	AND O2.OrderID = OL2.OrderID
    AND OL2.OrderedQuantity = 
    	(SELECT MIN(OL.OrderedQuantity)
         FROM OrderLine_T OL)
ORDER BY 3;

-- Conditional expressions
-- What products are included in ProductLine 1?
SELECT 
	CASE
		WHEN ProductLineID = 1 THEN ProductDescription
    ELSE '####'
    END AS ProductDescription
FROM Product_T;

-- For each salesperson, list their biggest-selling product
-- Tip: Define VIEW, then query against it
CREATE VIEW Tsales AS
	SELECT SP.SalespersonName, P.ProductDescription, SUM(OL.OrderedQuantity) AS TotOrders
    FROM Salesperson_T SP, OrderLine_T OL, Product_T P, Order_T O
    WHERE SP.SalespersonID = O.SalespersonID
    	AND O.OrderID = OL.OrderLineID
        AND OL.ProductID = P.ProductID
    GROUP BY SP.SalespersonName, P.ProductDescription;
      
SELECT A.SalespersonName, A.ProductDescription
FROM Tsales A
WHERE A.Totorders = 
	(SELECT MAX(B.Totorders)
     FROM Tsales B
     WHERE B.SalespersonName = A.SalespersonName);

-- List all salespersons who work in the territory where the most 'End Table's have been sold
-- USE Pine_Valley
CREATE TABLE TopTerritory
	SELECT T.TerritoryID, SUM(OL.OrderedQuantity) TotSales
    FROM Territory_T T, Customer_T C, DoesBusinessIn_T DBI, OrderLine_T OL, Order_T O, Product_T P
    WHERE C.CustomerID = DBI.CustomerID
    	AND O.OrderID = OL.OrderID
        AND C.CustomerID = O.CustomerID
        AND P.ProductID = OL.ProductID
        AND T.TerritoryID = DBI.TerritoryID
        AND P.ProductDescription = 'End Table'
    GROUP BY T.TerritoryID
    ORDER BY TotSales DESC
    LIMIT 1;

SELECT SP.SalespersonID, SP.SalespersonName
FROM Territory_T T
JOIN Salesperson_T SP ON
	T.TerritoryID = SP.SalesTerritoryID
WHERE SP.SalesTerritoryID IN
	(SELECT TerritoryID
     FROM TopTerritory);