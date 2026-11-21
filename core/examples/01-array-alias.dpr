program ArrayAlias;
{$APPTYPE CONSOLE}
type TNumbers = array of Integer;
var A, B: TNumbers;
begin
  SetLength(A, 1);
  A[0] := 4;
  B := A;
  B[0] := 9;
  Writeln(A[0]);
  SetLength(B, Length(B));
  B[0] := 12;
  Writeln(A[0]);
  Writeln(B[0]);
end.
