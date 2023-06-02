INSERT INTO "config" ("key", "value")
VALUES
  ('known_token',  '71a4f4dac32e3364c7ddc7c14'),
  ('known_admin', 'e2fa61f2d17574483f7')
;

INSERT INTO "user" ("name", "token")
VALUES
  ('test',  'f2d17574483f7ffbb431b4acb2f'),
  ('other', 'eaca413f27f2ecb76d6168407af')
;

INSERT INTO "product" ("id", "uuid", "name", "desc", "deleted")
VALUES
  (1, 'd5gf4sdg65g486df46gh6dfs4', 'product 1', 'eeheeh', NULL),
  (2, '25q4tawz4q34dhjplerhz54er', 'product 2', 'blabla', NULL),
  (3, '25q4tawz4q34dhjplerhz54er', 'product 3', 'blabla', '2023-01-01 00:00:00'),
  (4, 'ag534h6dj14t23k54h25dfj5f', 'product 4', '', NULL)
;

INSERT INTO "product_offers" ("product_id", "price", "pieces", "added")
VALUES
  (2, 159, 5, '2023-05-05 00:00:00'),
  (2, 756, 11, '2023-05-05 00:00:00'),
  (4, 351, 2, '2023-05-05 00:00:00'),
  (3, 556, 8, '2023-05-05 00:00:00')
;
