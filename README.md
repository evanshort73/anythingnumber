# AnythingNumber
Vocola extention to parse `<_anything>` variable as an integer

If you've ever created a large range of numbers in Vocola, like
```
<n> := 0..1000;
```
you've probably seen the error `natlink.BadGrammar: The grammar is too complex to be recognized`. AnythingNumber is a workaround for that problem.

Example Vocola command using AnythingNumber:
```
leap <_anything> =
  If(AnythingNumber.Validate($1),
     {ctrl+g} AnythingNumber.Convert($1) {enter} {end});
```

To install: Put `vocola_ext_anything_number.py` in your Vocola extensions directory (`/NatLink/NatLink/Vocola/extensions`).
