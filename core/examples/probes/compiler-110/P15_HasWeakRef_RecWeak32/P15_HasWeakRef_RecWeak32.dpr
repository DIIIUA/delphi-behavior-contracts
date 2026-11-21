program P15_HasWeakRef_RecWeak32;
{$APPTYPE CONSOLE}
uses System.SysUtils;
type
  TWeakIntfRec = record
    [weak] F: IInterface;
  end;
  TUnsafeIntfRec = record
    [unsafe] F: IInterface;
  end;
begin
  Writeln('TWeakIntfRec=', BoolToStr(HasWeakRef(TWeakIntfRec), True));
  Writeln('TUnsafeIntfRec=', BoolToStr(HasWeakRef(TUnsafeIntfRec), True));
end.
