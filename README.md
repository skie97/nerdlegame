# nerdlegame
Basically a text based solver for the nerdle game.

## General Idea
The general idea is to generate all possible sequences and solutions to the game.
One limitation that was imposed was not to start with a negative number.
But, it is possible for the answer to be negative.
It takes about 1.5 mins to generate that solution space of
61879 so this is stored as a solspace.csv.

Next, score each of the sequences based on the number of unique digits
and operators. The highest number is of course 8.
There are actually a total of 3667 such sequences.
We will randomly pick one of these as the seed.

The next couple of steps is simply a logic puzzle
using set theory. For each type of response,
we generate the required boolean vector and filter
the pandas dataframe.

For<span style="background-color:#161803"> black </span>, we generate the vectors for the number not to appear at all.

For<span style="background-color:#398874"> green </span>, we generate the vector for that position to have that number.

For<span style="background-color:#820458"> red </span>, we consider the negation of the contrapositive cause it's easier.
Say in this case, if the number exists in another position, it's troublesome
to construct the vectors directly. It's easier to consider the contrapositive.
i.e. the number doesn't exist in all other positions.
And negate that vector, together with the vector where that position doesn't have the number.

The dataframe will shrink until there is only one answer.

### TODO:
- Need to have a path for a random guess for the second try based on the first to get better performance.
