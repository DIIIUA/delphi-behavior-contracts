program P15_IsConstValue_CallOff32;
{$APPTYPE CONSOLE}

function ProbeInline(X: Integer): Boolean; inline;
begin
  Result := IsConstValue(X);
end;

{$PUSHOPT}{$INLINE OFF}
function CallWithInlineOff: Boolean;
begin
  Result := ProbeInline(42);
end;
{$POPOPT}

var
  BodyOff: Boolean;
begin
  Writeln('calloff_lit=', CallWithInlineOff);
  {$PUSHOPT}{$INLINE OFF}
  BodyOff := ProbeInline(42);
  {$POPOPT}
  Writeln('inloff_inline_body=', BodyOff);
end.
