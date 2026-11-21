program P15_DynArray_Ops32;
{$APPTYPE CONSOLE}
uses
  System.SysUtils;

function ArrStr(const Arr: TArray<Integer>): string;
var
  I: Integer;
begin
  Result := '[';
  for I := 0 to High(Arr) do
  begin
    if I > 0 then
      Result := Result + ',';
    Result := Result + IntToStr(Arr[I]);
  end;
  Result := Result + ']';
end;

var
  A, B, C, D, E, Alias, Alias2, Alias3, Alias4: TArray<Integer>;
begin
  A := [1, 2, 3];
  B := [4, 5];
  C := A + B;
  D := Concat(A, B, [6]);
  Writeln('C_plus=', ArrStr(C));
  Writeln('D_concat=', ArrStr(D));

  Insert(99, C, 1);
  Writeln('C_ins1=', ArrStr(C));
  Insert([77, 88], C, 0);
  Writeln('C_ins_sub=', ArrStr(C));
  Delete(C, 2, 2);
  Writeln('C_del=', ArrStr(C));
  E := Copy(C, 1, 3);
  Writeln('E_copy=', ArrStr(E));

  Alias := A;
  Alias[0] := 10;
  Writeln('A_after_alias=', ArrStr(A));

  Alias2 := A;
  Insert(55, Alias2, 0);
  Writeln('A_after_insert=', ArrStr(A), ';Alias2=', ArrStr(Alias2));

  Alias3 := A;
  Delete(Alias3, 0, 1);
  Writeln('A_after_delete=', ArrStr(A), ';Alias3=', ArrStr(Alias3));

  Alias4 := A;
  SetLength(Alias4, 5);
  Writeln('A_after_setlength=', ArrStr(A), ';Alias4_len=', Length(Alias4));
end.
