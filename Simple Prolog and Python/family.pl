/* dynamic rules  */

:- dynamic parent/2.
:- dynamic father/2.
:- dynamic mother/2.
:- dynamic sibling/2.
:- dynamic sister/2.
:- dynamic brother/2.
:- dynamic grandchild/2.
:- dynamic grandmother/2.
:- dynamic grandfather/2.
:- dynamic child/2.
:- dynamic daughter/2.
:- dynamic son/2.
:- dynamic aunt/2.
:- dynamic uncle/2.
:- dynamic relative/2.

:- dynamic male/1.
:- dynamic female/1.

:- dynamic parent_raw/2.

:- discontiguous child/2.

/* rules */

% Helper predicate to check if a relationship already exists
relationship_exists(Relationship, X, Y) :-
    Term =.. [Relationship, X, Y],
    clause(Term, _).

parent(X, Y) :-
    parent_raw(X, Y),
    X \= Y,
    \+parent_raw(Y, X).

% Updated mother rule
mother(X, Y) :-
    parent(X, Y),
    female(X),
    X \= Y,
    \+relationship_exists(mother, X, Y).

% Updated father rule
father(X, Y) :-
    parent(X, Y),
    male(X),
    X \= Y,
    \+relationship_exists(father, X, Y).

% Updated child rule
child(X, Y) :-
    parent(Y, X),
    X \= Y,
    \+relationship_exists(child, X, Y).

% Updated sibling rule
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y,
    \+relationship_exists(sibling, X, Y).

% Updated sister rule
sister(X, Y) :-
    sibling(X, Y),
    female(X),
    X \= Y,
    \+relationship_exists(sister, X, Y).

% Updated brother rule
brother(X, Y) :- 
    sibling(X, Y),
    male(X),
    X \= Y,
    \+relationship_exists(brother, X, Y).

% Updated child rule
child(X, Y) :-
    parent(Y, X),
    X \= Y,
    \+relationship_exists(child, X, Y).

% Updated partner rule
partner(X, Y) :-
    child(Z, X),
    child(Z, Y),
    X \= Y,
    \+relationship_exists(partner, X, Y).

% Updated uncle rule
uncle(X, Y) :-
    brother(X, Z),
    child(Y, Z),
    X \= Y,
    \+relationship_exists(uncle, X, Y).

% Updated aunt rule
aunt(X, Y) :-
    sister(X, Z),
    child(Y, Z),
    X \= Y,
    \+relationship_exists(aunt, X, Y).


% Updated cousin rule
cousin(X, Y) :-
    grandparent(Z, X),
    grandparent(Z, Y),
    \+sibling(X, Y),
    X \= Y,
    \+relationship_exists(cousin, X, Y).

% Updated nephew rule
nephew(X, Y) :-
    (aunt(Y, X) ; uncle(Y, X)),
    male(X),
    X \= Y,
    \+relationship_exists(nephew, X, Y).

% Updated niece rule
niece(X, Y) :-
    (aunt(Y, X) ; uncle(Y, X)),
    female(X),
    X \= Y,
    \+relationship_exists(niece, X, Y).




% Updated relative rule
relative(X, Y) :-
    parent(X, Y).
relative(X, Y) :-
    parent(Y, X).
relative(X, Y) :-
    sibling(X, Y).
relative(X, Y) :-
    sibling(Y, X).
relative(X, Y) :-
    aunt(X, Y).
relative(X, Y) :-
    aunt(Y, X).
relative(X, Y) :-
    uncle(X, Y).
relative(X, Y) :-
    uncle(Y, X).
relative(X, Y) :-
    cousin(X, Y).
relative(X, Y) :-
    cousin(Y, X).
relative(X, Y) :-
    nephew(X, Y).
relative(X, Y) :-
    nephew(Y, X).
relative(X, Y) :-
    niece(X, Y).
relative(X, Y) :-
    niece(Y, X).
relative(X, Y) :-
    grandparent(X, Y).
relative(X, Y) :-
    grandparent(Y, X).
relative(X, Y) :-
    partner(X, Y).
relative(X, Y) :-
    partner(Y, X).
