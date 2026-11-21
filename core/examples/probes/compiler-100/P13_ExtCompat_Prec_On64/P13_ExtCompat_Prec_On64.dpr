program P13_ExtCompat_Prec_On64;
{$APPTYPE CONSOLE}
{$EXTENDEDCOMPATIBILITY ON}
uses
  System.SysUtils;

type
  TUnpacked = record
    A: Byte;
    E: Extended;
    B: Byte;
  end;

  TPacked = packed record
    A: Byte;
    E: Extended;
    B: Byte;
  end;

var
  U: TUnpacked;
  P: TPacked;
  E1, E2, E3: Extended;
  R80: TExtended80Rec;
  RawSrc, RawDst: array[0..15] of Byte;
  I: Integer;
  HexSrc, HexDst: string;
begin
  Writeln('SizeOf(Extended)=', SizeOf(Extended));
  Writeln('Unpacked=', SizeOf(TUnpacked), ';offE=', NativeUInt(@U.E) - NativeUInt(@U), ';offB=', NativeUInt(@U.B) - NativeUInt(@U));
  Writeln('Packed=', SizeOf(TPacked), ';offE=', NativeUInt(@P.E) - NativeUInt(@P), ';offB=', NativeUInt(@P.B) - NativeUInt(@P));
  Writeln('SizeOf(TExtended80Rec)=', SizeOf(TExtended80Rec));

  E1 := 1.0 + ParamCount * 0.0;
  E2 := 1e-17 + ParamCount * 0.0;
  E3 := E1 + E2;
  Writeln('prec64=', E3 <> E1);

  FillChar(RawSrc, SizeOf(RawSrc), 0);
  FillChar(RawDst, SizeOf(RawDst), 0);
  E1 := 123.45678901234567;
  Move(E1, RawSrc[0], SizeOf(Extended));
  R80 := TExtended80Rec(E1);
  E2 := Extended(R80);
  Move(E2, RawDst[0], SizeOf(Extended));
  HexSrc := '';
  HexDst := '';
  for I := 0 to SizeOf(Extended) - 1 do
  begin
    HexSrc := HexSrc + IntToHex(RawSrc[I], 2);
    HexDst := HexDst + IntToHex(RawDst[I], 2);
  end;
  Writeln('rt_eq=', HexSrc = HexDst, ';bytes=', HexSrc);
end.
