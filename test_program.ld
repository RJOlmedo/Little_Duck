PROGRAM TestProgram;
VAR
  a, b : int;
  c : float;
BEGIN
  a = 10;
  b = 20;
  c = a + b;
  IF (a > b) THEN
    PRINT("a is greater");
  ELSE
    PRINT("b is greater");
  WHILE (a < 100) DO
    a = a + 1;
END
