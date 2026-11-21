-- The demo fleet, a demo driver and the launch promo code.
INSERT INTO cars (id, name, category, transmission, seats, daily_fils) VALUES
    (1, 'Kia Picanto', 'economy', 'manual', 4, 8000),
    (2, 'Hyundai i10', 'economy', 'automatic', 4, 8500),
    (3, 'Nissan Sunny', 'economy', 'automatic', 5, 9000),
    (4, 'Toyota Yaris', 'economy', 'automatic', 5, 10000),
    (5, 'Suzuki Swift', 'economy', 'manual', 5, 9500),
    (6, 'Mitsubishi Attrage', 'economy', 'automatic', 5, 8800),
    (7, 'Chevrolet Spark', 'economy', 'manual', 4, 7500),
    (8, 'Kia Rio', 'economy', 'automatic', 5, 10500),
    (9, 'Toyota Corolla', 'compact', 'automatic', 5, 13000),
    (10, 'Honda Civic', 'compact', 'automatic', 5, 14000),
    (11, 'Hyundai Elantra', 'compact', 'automatic', 5, 13500),
    (12, 'Mazda 3', 'compact', 'automatic', 5, 14500),
    (13, 'Volkswagen Golf', 'compact', 'manual', 5, 15000),
    (14, 'Kia Cerato', 'compact', 'automatic', 5, 12500),
    (15, 'Toyota RAV4', 'suv', 'automatic', 5, 20000),
    (16, 'Nissan X-Trail', 'suv', 'automatic', 7, 22000),
    (17, 'Hyundai Tucson', 'suv', 'automatic', 5, 19000),
    (18, 'Mitsubishi Pajero', 'suv', 'manual', 7, 24000),
    (19, 'Toyota Land Cruiser', 'suv', 'automatic', 8, 45000),
    (20, 'Kia Sorento', 'suv', 'automatic', 7, 23000),
    (21, 'Ford Explorer', 'suv', 'automatic', 7, 28000),
    (22, 'Toyota Hiace', 'van', 'manual', 12, 30000),
    (23, 'Hyundai Staria', 'van', 'automatic', 9, 32000),
    (24, 'Mercedes E-Class', 'luxury', 'automatic', 5, 40000),
    (25, 'BMW 5 Series', 'luxury', 'automatic', 5, 42000),
    (26, 'Lexus ES', 'luxury', 'automatic', 5, 38000),
    (27, 'Range Rover Sport', 'luxury', 'automatic', 5, 60000),
    (28, 'Mazda MX-5', 'sports', 'manual', 2, 26000),
    (29, 'Ford Mustang', 'sports', 'automatic', 4, 35000),
    (30, 'Nissan Patrol', 'suv', 'automatic', 8, 48000);

INSERT INTO drivers (id, name, birth_date, licence) VALUES
    (1, 'Demo Driver', '1990-05-14', 'BH-1990-0001');

INSERT INTO promos (code, percent) VALUES
    ('WELCOME10', 10);
