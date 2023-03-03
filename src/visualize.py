#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()


# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
orig_dict = dict(sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True))
#for k,v in items:
  # print(k,':',v)

# Top 10 keys
top_ten = dict(reversed(sorted(orig_dict.items(), key = lambda x: x[1], reverse=True)[:10]))
key = []
value = []

print("Top 10" + str(top_ten))

#Plotting
plt.bar(range(len(top_ten)), list(top_ten.values()), align='center')
plt.xticks(range(len(top_ten)), list(top_ten.keys()))

plt.show()

# if statements for lang/country
if args.input_path == "reduced.lang":
    plt.xlabel("Language")
    plt.ylabel("Tweets with" + args.key)
else:
    plt.xlabel("Country")
    plt.ylabel("Tweets with" + args.key)


# Save bar graph as png
plt.savefig("./plots/" + args.input_path + args.key + '.png')

