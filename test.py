import random

text = "Hello"
smp = "".join( random.choice([k.upper(), k ]) for k in text )
print(smp)