drop database MOBILE_ANALYTICS_PROJECT ;
CREATE DATABASE MOBILE_ANALYTICS_PROJECT ;
USE MOBILE_ANALYTICS_PROJECT ;
/*TABLE NAME : smartphones
COLUMN : brand_name, model,price,avg_rating,5G_or_not,processor_brand,num_cores,processor_speed,battery_capacity,
 fast_charging_available,fast_charging,ram_capacity,internal_memory,screen_size,refresh_rate,num_rear_cameras,
 os,primary_camera_rear,primary_camera_front,extended_memory_available,resolution_height,resolution_width */

drop procedure if exists Dimension_Tables; 
DELIMITER // 
CREATE PROCEDURE Dimension_Tables() 
     BEGIN 
     SET FOREIGN_KEY_CHECKS = 0;
     -- Dim_Brand
     DROP TABLE IF EXISTS Dim_Brand ;
CREATE TABLE Dim_Brand (
             brand_id INT PRIMARY KEY AUTO_INCREMENT,
             brand_name VARCHAR(100) UNIQUE not null ); 
INSERT INTO Dim_Brand (brand_name) 
SELECT DISTINCT brand_name From smartphones;
	
    --  Dim_Model 
	DROP TABLE IF EXISTS Dim_Model ;
 CREATE TABLE Dim_Model (
              model_id INT PRIMARY KEY AUTO_INCREMENT, 
              model_name VARCHAR(100) not null, 
              brand_id int not null,
              foreign key (brand_id) references  Dim_Brand (brand_id)
              ); 
			
 INSERT INTO Dim_Model (model_name, brand_id)
SELECT DISTINCT s.model, b.brand_id
FROM smartphones s
JOIN Dim_Brand b ON s.brand_name = b.brand_name;
        
        --  Dim_Processor;
         DROP TABLE IF EXISTS Dim_Processor; 
CREATE TABLE Dim_Processor (
                Processor_id INT PRIMARY KEY AUTO_INCREMENT, 
                Processor_brand VARCHAR(100)  NOT NULL,
                num_cores int  not null, 
                processor_speed decimal(4,2) ); 
INSERT INTO Dim_Processor (Processor_brand,num_cores,processor_speed) 
SELECT DISTINCT processor_brand,num_cores,processor_speed 
      From smartphones;
      
      -- Dim_Battery;
	   DROP TABLE IF EXISTS Dim_Battery;
CREATE TABLE Dim_Battery ( 
			   battery_id INT PRIMARY KEY AUTO_INCREMENT,
               battery_capacity int  NOT NULL,
               fast_charging_available int  not null, 
               fast_charging int  not null );
               
INSERT INTO Dim_Battery ( battery_capacity,fast_charging_available,fast_charging) 
SELECT DISTINCT battery_capacity,fast_charging_available,fast_charging From smartphones; 
         
        --  Dim_Memory; 
		DROP TABLE IF EXISTS Dim_Memory; 
CREATE TABLE Dim_Memory (
			memory_id INT PRIMARY KEY AUTO_INCREMENT,
            ram_capacity int  NOT NULL, 
            internal_memory int  not null, 
            extended_memory_available int not null ); 
            
INSERT INTO Dim_Memory (ram_capacity,internal_memory,extended_memory_available )
 SELECT DISTINCT ram_capacity,internal_memory,extended_memory_available From smartphones; 
       
       --  Dim_Display
       DROP TABLE IF EXISTS Dim_Display; 
CREATE TABLE Dim_Display ( 
          display_id INT PRIMARY KEY AUTO_INCREMENT, 
          screen_size decimal(4,2) NOT NULL,
          refresh_rate int  not null,
          resolution_height int  not null,
          resolution_width int not null );
          
INSERT INTO Dim_Display (screen_size,refresh_rate, resolution_height,resolution_width)
 SELECT DISTINCT screen_size,refresh_rate, resolution_height,resolution_width From smartphones; 
        
        -- Dim_Camera
        DROP TABLE IF EXISTS Dim_Camera; 
CREATE TABLE Dim_Camera ( 
		 camera_id INT PRIMARY KEY AUTO_INCREMENT, 
         num_rear_cameras int  NOT NULL, 
         primary_camera_rear int  not null,
         primary_camera_front int  not null );
         
  INSERT INTO Dim_Camera (num_rear_cameras,primary_camera_rear,primary_camera_front) 
  SELECT DISTINCT num_rear_cameras,primary_camera_rear,primary_camera_front From smartphones; 
            
            --  Dim_OS
           DROP TABLE IF EXISTS Dim_OS;
CREATE TABLE Dim_OS( 
         os_id INT PRIMARY KEY AUTO_INCREMENT, 
         os varchar(100) not null ); 
INSERT INTO Dim_OS (os) SELECT DISTINCT os From smartphones;

         SET FOREIGN_KEY_CHECKS = 1;  
 END //
 DELIMITER ; 
SET GLOBAL net_read_timeout = 300;
 SET GLOBAL net_write_timeout = 300;
 SET GLOBAL max_allowed_packet = 1073741824;
SET SESSION net_read_timeout = 300;
 SET SESSION net_write_timeout = 300;
SET SESSION wait_timeout = 600;
SET SESSION interactive_timeout = 600;
 CALL Dimension_Tables();  

	-- FACT_TABLE
DROP PROCEDURE IF EXISTS FACT_OF_TABLE;
DELIMITER //
CREATE PROCEDURE FACT_OF_TABLE()
BEGIN
  DROP TABLE IF EXISTS FACT_TABLE;

  CREATE TABLE FACT_TABLE (
    smartphone_id INT AUTO_INCREMENT PRIMARY KEY,
    price INT,
    avg_rating DOUBLE,
    is_5G TINYINT(1),
    brand_id INT,
    model_id INT,
    processor_id INT,
    battery_id INT,
    memory_id INT,
    display_id INT,
    camera_id INT,
    os_id INT,
    FOREIGN KEY (brand_id)   REFERENCES Dim_Brand(brand_id),
    FOREIGN KEY (model_id)   REFERENCES Dim_Model(model_id),
    FOREIGN KEY (processor_id) REFERENCES Dim_Processor(processor_id),
    FOREIGN KEY (battery_id) REFERENCES Dim_Battery(battery_id),
    FOREIGN KEY (memory_id)  REFERENCES Dim_Memory(memory_id),
    FOREIGN KEY (display_id) REFERENCES Dim_Display(display_id),
    FOREIGN KEY (camera_id)  REFERENCES Dim_Camera(camera_id),
    FOREIGN KEY (os_id)      REFERENCES Dim_OS(os_id)
  );

  INSERT INTO FACT_TABLE (price, avg_rating, is_5G, brand_id, model_id, processor_id, battery_id,
                          memory_id, display_id, camera_id, os_id)
  WITH
  dedup AS (
    SELECT s.*,
           ROW_NUMBER() OVER (
             PARTITION BY COALESCE(s.brand_name,''), COALESCE(s.model,''), COALESCE(s.price,0),
                          COALESCE(s.avg_rating,0), COALESCE(s.is_5G,0),
                          COALESCE(s.processor_brand,''), COALESCE(s.num_cores,0), COALESCE(s.processor_speed,0),
                          COALESCE(s.battery_capacity,0), COALESCE(s.fast_charging_available,0), COALESCE(s.fast_charging,0),
                          COALESCE(s.ram_capacity,0), COALESCE(s.internal_memory,0), COALESCE(s.extended_memory_available,0),
                          COALESCE(s.screen_size,0), COALESCE(s.refresh_rate,0), COALESCE(s.resolution_height,0), COALESCE(s.resolution_width,0),
                          COALESCE(s.num_rear_cameras,0), COALESCE(s.primary_camera_rear,0), COALESCE(s.primary_camera_front,0), COALESCE(s.os,'')
             ORDER BY s.price
           ) AS rn
    FROM smartphones s
  ),
  filtered AS (
    SELECT * FROM dedup WHERE rn = 1
  ),
  brand_u AS (
    SELECT MIN(brand_id) AS brand_id, brand_name FROM Dim_Brand GROUP BY brand_name
  ),
  model_u AS (
    SELECT MIN(model_id) AS model_id, model_name, brand_id FROM Dim_Model GROUP BY model_name, brand_id
  ),
  processor_u AS (
    SELECT MIN(processor_id) AS processor_id, processor_brand, num_cores, processor_speed
    FROM Dim_Processor GROUP BY processor_brand, num_cores, processor_speed
  ),
  battery_u AS (
    SELECT MIN(battery_id) AS battery_id, battery_capacity, fast_charging_available, fast_charging
    FROM Dim_Battery GROUP BY battery_capacity, fast_charging_available, fast_charging
  ),
  memory_u AS (
    SELECT MIN(memory_id) AS memory_id, ram_capacity, internal_memory, extended_memory_available
    FROM Dim_Memory GROUP BY ram_capacity, internal_memory, extended_memory_available
  ),
  display_u AS (
    SELECT MIN(display_id) AS display_id, screen_size, refresh_rate, resolution_height, resolution_width
    FROM Dim_Display GROUP BY screen_size, refresh_rate, resolution_height, resolution_width
  ),
  camera_u AS (
    SELECT MIN(camera_id) AS camera_id, num_rear_cameras, primary_camera_rear, primary_camera_front
    FROM Dim_Camera GROUP BY num_rear_cameras, primary_camera_rear, primary_camera_front
  ),
  os_u AS (
    SELECT MIN(os_id) AS os_id, os FROM Dim_OS GROUP BY os
  )
  SELECT
    f.price,
    f.avg_rating,
    CASE WHEN LOWER(COALESCE(f.is_5G,'')) IN ('1','true','yes','y') THEN 1
         WHEN f.is_5G = 1 THEN 1
         ELSE 0 END AS is_5G,
    b.brand_id,
    m.model_id,
    p.processor_id,
    bt.battery_id,
    mem.memory_id,
    d.display_id,
    c.camera_id,
    o.os_id
  FROM filtered f
  LEFT JOIN brand_u b ON f.brand_name = b.brand_name
  LEFT JOIN model_u m ON f.model = m.model_name AND m.brand_id = b.brand_id
  LEFT JOIN processor_u p ON COALESCE(f.processor_brand,'') = COALESCE(p.processor_brand,'')
                        AND (COALESCE(f.num_cores,0) = COALESCE(p.num_cores,0))
                        AND (COALESCE(f.processor_speed,0) = COALESCE(p.processor_speed,0))
  LEFT JOIN battery_u bt ON COALESCE(f.battery_capacity,0) = COALESCE(bt.battery_capacity,0)
                        AND COALESCE(f.fast_charging_available,0) = COALESCE(bt.fast_charging_available,0)
                        AND COALESCE(f.fast_charging,0) = COALESCE(bt.fast_charging,0)
  LEFT JOIN memory_u mem ON COALESCE(f.ram_capacity,0) = COALESCE(mem.ram_capacity,0)
                        AND COALESCE(f.internal_memory,0) = COALESCE(mem.internal_memory,0)
                        AND COALESCE(f.extended_memory_available,0) = COALESCE(mem.extended_memory_available,0)
  LEFT JOIN display_u d ON COALESCE(f.screen_size,0) = COALESCE(d.screen_size,0)
                       AND COALESCE(f.refresh_rate,0) = COALESCE(d.refresh_rate,0)
                       AND COALESCE(f.resolution_height,0) = COALESCE(d.resolution_height,0)
                       AND COALESCE(f.resolution_width,0) = COALESCE(d.resolution_width,0)
  LEFT JOIN camera_u c ON COALESCE(f.num_rear_cameras,0) = COALESCE(c.num_rear_cameras,0)
                      AND COALESCE(f.primary_camera_rear,0) = COALESCE(c.primary_camera_rear,0)
                      AND COALESCE(f.primary_camera_front,0) = COALESCE(c.primary_camera_front,0)
  LEFT JOIN os_u o ON COALESCE(f.os,'') = COALESCE(o.os,'');

END //
DELIMITER ;
call FACT_OF_TABLE() ;
select count(*) from fact_table ;


/*7. Analytical Questions:
1. Total Sales and Average Price by Brand.
2. Top 5 Smartphones by Rating and Price.
3. Smartphone Price Distribution by Brand and OS.
4. Market Share by Brand and Processor Speed.
5. Number of Models and Avg Price by RAM Size and Bran
6.Top 3 Fastest Charging Smartphones by Price.
7. Brand Performance by 5G Availability.
8. Correlation Between Processor Speed and Price by Brand.
9. Price-to-Performance Ratio by Brand.
10. Most Popular Display Features.
11. Multi-Feature Ranking (Composite Score).
12. Average Battery Capacity and Fast-Charging Comparison by OS.*/
                
              
  -- 1. Total Sales and Average Price by Brand.  
SELECT 
    b.brand_name AS brand_name,
    COUNT(*) AS total_units,
    SUM(f.price) AS total_sales,
    AVG(f.price) AS avg_price
FROM
    fact_table AS f
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
GROUP BY brand_name
ORDER BY total_sales DESC;

-- 2. Top 5 Smartphones by Rating and Price.
SELECT 
    f.smartphone_id AS smartphones,
    b.brand_name AS brand_name,
    m.model_name AS model_name,
    f.avg_rating AS rating,
    f.price AS price
FROM
    fact_table AS f
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        JOIN
    dim_model AS m ON f.model_id = m.model_id
ORDER BY rating DESC , price DESC
LIMIT 5;

-- 3. Smartphone Price Distribution by Brand and OS.

SELECT 
    b.brand_name,
    o.os,
    COUNT(*) AS N,
    MIN(f.price) AS min_price,
    MAX(f.price) AS max_price,
    ( MAX(f.price) - min(f.price) ) AS price_range,
    AVG(f.price) AS avg_price,
   sum(f.price) / (SELECT SUM( fact_table.price)
        from
         fact_table) * 100 AS percentage
FROM
    fact_table AS f
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        JOIN
    dim_os AS o ON f.os_id = o.os_id
GROUP BY b.brand_name , o.os
ORDER BY b.brand_name , o.os;





-- 4. Market Share by Brand and Processor Speed.
SELECT 
    b.brand_name,
    CASE
        WHEN p.processor_speed >= 3 THEN 'high'
        WHEN p.processor_speed >= 2 THEN 'mediam'
        WHEN p.processor_speed > 1 THEN 'low'
        ELSE 'Unknown'
    END AS speed_bucket,
    COUNT(*) AS units,
    ROUND(COUNT(*) / (SELECT 
                    COUNT(*)
                FROM
                    fact_table) * 100,
            2) AS market_share_per_unit
FROM
    fact_table AS f
        JOIN
    dim_processor AS p ON f.Processor_id = p.Processor_id
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
GROUP BY b.brand_name , speed_bucket
ORDER BY market_share_per_unit DESC;
         
-- 5. Number of Models and Avg Price by RAM Size and Brand.
SELECT 
    b.brand_name,
    me.ram_capacity AS ram_size,
    COUNT(DISTINCT m.model_name) num_models,
    AVG(f.price) AS Avg_price
FROM
    fact_table AS f
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        JOIN
    dim_memory AS me ON f.memory_id = me.memory_id
        JOIN
    dim_model AS m ON f.model_id = m.model_id
GROUP BY b.brand_name , ram_size
ORDER BY b.brand_name , ram_size DESC;


-- 6.Top 3 Fastest Charging Smartphones by Price.
SELECT 
    b.brand_name, m.model_name, ba.fast_charging,ba.battery_capacity, f.price
FROM
    fact_table AS f
        JOIN
    dim_battery AS ba ON f.battery_id = ba.battery_id
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        JOIN
    dim_model AS m ON f.model_id = m.model_id
ORDER BY  ba.fast_charging desc,f.price DESC
LIMIT 3;

-- 7. Brand Performance by 5G Availability.

SELECT b.brand_name,m.model_name,f.is_5G,avg(f.price) as avg_price,avg(f.avg_rating) as avg_rating
from fact_table as f 
join dim_brand as b
on f.brand_id=b.brand_id
join dim_model as m
on f.model_id =m.model_id
GROUP BY b.brand_name,m.model_name,f.is_5G
order by f.is_5G desc ;

SELECT b.brand_name,
       f.is_5G,
       COUNT(*) AS cnt,
       AVG(f.price) AS avg_price,
       AVG(f.avg_rating) AS avg_rating
FROM fact_table f
JOIN Dim_Brand b ON f.brand_id = b.brand_id
GROUP BY b.brand_name, f.is_5G
ORDER BY b.brand_name, f.is_5G DESC;

-- 8. Correlation Between Processor Speed and Price by Brand.  
 
WITH procease AS (
SELECT 
    b.brand_name AS brand_name,
    p.processor_speed AS x,
    f.price AS y,
    p.processor_speed * f.price AS xy,
    p.processor_speed * p.processor_speed AS x2,
    f.price * f.price AS y2
FROM
    fact_table AS f
        JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        JOIN
    dim_processor AS p ON f.Processor_id = p.Processor_id),
  correlation AS (
   SELECT 
    brand_name,
    (
    (SUM(xy) - (SUM(x) * SUM(y) / COUNT(*))) / 
                   SQRT(
                                 (SUM(x2) - (SUM(x) * SUM(x) / COUNT(*))) *
                                  (SUM(y2) - (SUM(y) * SUM(y) / COUNT(*)))
                         )
    ) AS relation
FROM
    procease
GROUP BY brand_name )
    SELECT 
    *
FROM
    correlation
ORDER BY relation DESC ;
    
-- 9. Price-to-Performance Ratio by Brand.

SELECT 
    b.brand_name,
    AVG(
    (p.processor_speed * p.num_cores + me.ram_capacity / 4 
    + c.primary_camera_rear / 10 + ba.battery_capacity) /
    f.price) AS avg_ppr
FROM
    fact_table AS f
        LEFT JOIN
    dim_brand AS b ON f.brand_id = b.brand_id
        LEFT JOIN
    dim_memory AS me ON f.memory_id = me.memory_id
        LEFT JOIN
    dim_camera AS c ON f.camera_id = c.camera_id
        LEFT JOIN
    dim_battery AS ba ON f.battery_id = ba.battery_id
        LEFT JOIN
    dim_processor AS p ON f.Processor_id = p.Processor_id
GROUP BY b.brand_name
ORDER BY avg_ppr DESC;
    
-- 10. Most Popular Display Features.
SELECT d.screen_size, d.refresh_rate,
 CONCAT(d.resolution_height, 'x', d.resolution_width) AS resolution_combo,
       COUNT(*) AS num_models
FROM fact_table f
join dim_brand as b
on f.brand_id =b.brand_id
JOIN Dim_Display d ON f.display_id = d.display_id
GROUP BY d.screen_size, d.refresh_rate, resolution_combo
ORDER BY num_models DESC
LIMIT 10;

-- 11. Multi-Feature Ranking (Composite Score).
WITH metrics AS (
  SELECT f.smartphone_id, b.brand_name, m.model_name,
         p.processor_speed AS proc,
         p.num_cores as cores,
         mem.ram_capacity AS ram,
        bt.battery_capacity AS batt,
         f.avg_rating AS rating
  FROM fact_table f
  LEFT JOIN Dim_Processor p ON f.processor_id = p.processor_id
  LEFT JOIN Dim_Memory mem ON f.memory_id = mem.memory_id
  LEFT JOIN Dim_Battery bt ON f.battery_id = bt.battery_id
  LEFT JOIN Dim_Brand b ON f.brand_id = b.brand_id
  LEFT JOIN Dim_Model m ON f.model_id = m.model_id
),
norm AS (
  SELECT *,
    (proc - (SELECT MIN(proc) FROM metrics)) /
      (SELECT MAX(proc)-MIN(proc) FROM metrics)AS n_proc,
    (cores - (SELECT MIN(cores) FROM metrics)) /
      (SELECT MAX(cores)-MIN(cores) FROM metrics) AS n_core,
    (ram - (SELECT MIN(ram) FROM metrics)) /
      (SELECT MAX(ram)-MIN(ram) FROM metrics) AS n_ram,
    (batt - (SELECT MIN(batt) FROM metrics)) /
      (SELECT MAX(batt)-MIN(batt) FROM metrics) AS n_batt,
    (rating - (SELECT MIN(rating) FROM metrics)) /
      (SELECT MAX(rating)-MIN(rating) FROM metrics) AS n_rate
  FROM metrics
),
score AS (
  SELECT smartphone_id, brand_name, model_name,
         (0.3*n_proc + 0.1*n_core + 0.2*n_ram + 0.1*n_batt + 0.3*n_rate) AS comp_score
  FROM norm
)
SELECT smartphone_id,brand_name, model_name,
       ROUND(comp_score,4) AS composite_score,
       RANK() OVER (ORDER BY comp_score DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY comp_score DESC) AS dense_rnk
FROM score
ORDER BY comp_score DESC;


-- 12. Average Battery Capacity and Fast-Charging Comparison by OS.
SELECT 
    o.os,
    COUNT(*) AS n,
    AVG(bt.battery_capacity) AS avg_battery_capacity,
    AVG(bt.fast_charging) AS avg_fast_charging_power,
    SUM(bt.fast_charging_available) AS num_with_fast_charging,
    ROUND(100 * SUM(bt.fast_charging_available) / COUNT(*),
            2) AS pct_with_fast_charging
FROM
    fact_table f
        LEFT JOIN
    Dim_OS o ON f.os_id = o.os_id
        LEFT JOIN
    Dim_Battery bt ON f.battery_id = bt.battery_id
GROUP BY o.os
ORDER BY avg_battery_capacity DESC;

