demonsMale = ["Jealousy", "Wrath", "Tears", "Sighing", "Suffering", "Lamentation", "Bitter Weeping"]
demonsMaleModifier = ["Jealous", "Wrathful", "Tearful", "Sighing", "Suffering", "Lamenting", "Embittered Weeping"]

demonsFemale = ["Wrath", "Pain", "Lust", "Sighing", "Cursedness", "Bitterness", "Quarelsomeness"]
demonsFemaleModifier = ["Wrathful", "Painful", "Lusty", "Sighing", "Cursed", "Bitter", "Quarelsome"]

angelsMale = ["Unenviousness", "Blessedness", "Joy", "Truth", "Unbegrudgingness", "Belovedness", "Trustworthyness"]
angelsMaleModifier = ["Unenvious", "Blessed", "Joyful", "True", "Unbegrudging", "Beloved", "Trustworthy"]

angelsFemale = ["Peace", "Gladness", "Rejoicing", "Blessedness", "Truth", "Love", "Faith"]
angelsFemaleModifier = ["Peaceful", "Glad", "Rejoicing", "Blessed", "Truthful", "Lovely", "Faithful"]

gates = ["Calcination","Dissolution","Separation","Conjuction","Putrefaction","Congelation","Cibation","Sublimation","Fermentation","Exhaltation","Multiplication","Projection"]
gatesModifier = ["Calcinated","Dissolved","Separated","Conjucted","Putrid","Congealed","Cibated","Sublime","Fermented","Exhaltated","Multiplied","Projected"]

maleDemons = [demonsMale, demonsMaleModifier]
femaleDemons = [demonsFemale, demonsFemaleModifier]
maleAngels = [angelsMale, angelsMaleModifier]
femaleAngels = [angelsFemale, angelsFemaleModifier]
gates12 = [gates, gatesModifier]

md_fd = [maleDemons, femaleDemons]
fd_md = [femaleDemons, maleDemons]

ma_fa = [maleAngels, femaleAngels]
fa_ma = [femaleAngels, maleAngels]

md_fa = [maleDemons, femaleAngels]
fa_md = [femaleAngels, maleDemons]

ma_fd = [maleAngels, femaleDemons]
fd_ma = [femaleDemons, maleAngels]

md_12 = [maleDemons, gates12]
fd_12 = [femaleDemons, gates12]

demonArray = [
md_fd, 
md_fa, 
ma_fd, 
ma_fa, 
fd_md, 
fd_ma,
fa_md,
fa_ma
]

demonGates = [md_12, fd_12]

demonArrayName = [
"<b>The 49 Androgynous Demons</b><br> (from The 7 Androgynous Male Demons -x-  The 7 Androgynous Female Demons]",
"<b>The 49 Androgynous Cherubim</b><br> (from The 7 Androgynous Male Demons -x-  The 7 Androgynous Female Angels]",
"<b>The 49 Androgynous Cherubim</b><br> (from The 7 Androgynous Male Angels -x-  The 7 Androgynous Female Demons]",
"<b>The 49 Androgynous Angels</b><br>(from The 7 Androgynous Male Angels -x-  The 7 Androgynous Female Angels]",
"<b>The 49 Androgynous Demons</b><br> (from The 7 Androgynous Female Demons -x- The 7 Androgynous Male Demons]",
"<b>The 49 Androgynous Cherubim</b><br> (from The 7 Androgynous Female Demons -x- The 7 Androgynous Male Angels]",
"<b>The 49 Androgynous Cherubim</b><br> (from The 7 Androgynous Female Angels -x-  The 7 Androgynous Male Demons]",
"<b>The 49 Androgynous Angels</b><br> (from The 7 Androgynous Female Angels -x-  The 7 Androgynous Male Angels]"]

demonLookUp = ["md_fd", "md_fa", "ma_fd", "ma_fa", "fd_md", "fd_ma", "fa_md", "fa_ma"]
 
demonGatesName_X = ["The 7 Androgynous Male Demons", "The 7 Androgynous Female Demons"];
demonGatesName_Y = ["12 Gates of Sublime Transformation", "12 Gates of Sublime Transformation"];

demonGatesName = ["The 7 Androgynous Male Demons -x- 12 Gates of Sublime Transformation", "The 7 Androgynous Female Demons -x- 12 Gates of Sublime Transformation"];