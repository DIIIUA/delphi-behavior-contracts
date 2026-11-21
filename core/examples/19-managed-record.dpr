program ManagedRecord;
{$APPTYPE CONSOLE}
type
  TCounter = record
    Value: Integer;
    class operator Initialize(out Dest: TCounter);
    class operator Finalize(var Dest: TCounter);
  end;
var Finalized: Integer;
class operator TCounter.Initialize(out Dest: TCounter);
begin
  Dest.Value := 5;
end;
class operator TCounter.Finalize(var Dest: TCounter);
begin
  Inc(Finalized);
end;
procedure UseCounter;
var Counter: TCounter;
begin
  Writeln(Counter.Value);
end;
begin
  Finalized := 0;
  UseCounter;
  Writeln(Finalized);
end.
