# Chempiler: A convenient notation for chemistry problems

Note: The repo is in very early stages. Progress has been made on the notation spec and the parser, but the backend is not implemented yet. Check out the roadmap for more info.

The notation system's foundation is the disctintion between input (`given:`) and output (`find:`) information. This separation mirrors how chemists approach problems and how calculations naturally flow.

You can specify your knowns as a list of givens, followed by the information you're looking for in a `find:` statement.
```
given:
25.0g NaCl
250mL H2O
   
find: M NaCl
```

The compiler will make reasonable assumptions, perform the calculation, and report the assuptions back to the user. 
```
given:
250mL 0.500M NaCl
```
```
Assumptions:
solvent in NaCl solution = water
```

The user can override these assumptions.
```
given:
250mL 0.500M NaCl in ethanol
```

The simple notation makes complex stoichiometry a breeze.
```
given:
2 "egg" / 100.50g
6 "egg" / 1 "cake"
1 "cake" / 2 lb
12 "egg"

find: kg "cake"
find: g "egg"
```

## Roadmap
- [X] Initial notation design
- [X] Test driven workflow for parser implementation
- [ ] Full parser implmentaiton
- [ ] Compiler backend (utilizing libraries such as `chempy`
