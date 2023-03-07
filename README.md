# Coronavirus twitter analysis


## Background

Approximately 500 million tweets are sent everyday.
Of those tweets, about 1% are *geotagged*.
That is, the user's device includes location information about where the tweets were sent from.
The lambda server's `/data-fast/twitter\ 2020` folder contains all geotagged tweets that were sent in 2020.
In total, there are about 1.1 billion tweets in this dataset.
We can calculate the amount of disk space used by the dataset with the `du` command as follows:
```
$ du -h /data-fast/twitter\ 2020
```

The tweets are stored as follows.
The tweets for each day are stored in a zip file `geoTwitterYY-MM-DD.zip`,
and inside this zip file are 24 text files, one for each hour of the day.
Each text file contains a single tweet per line in JSON format.
JSON is a popular format for storing data that is closely related to python dictionaries.

Vim is able to open compressed zip files,
and I encourage you to use vim to explore the dataset.
For example, run the command
```
$ vim /data-fast/twitter\ 2020/geoTwitter20-01-01.zip
```
Or you can get a "pretty printed" interface with a command like
```
$ unzip -p /data-fast/twitter\ 2020/geoTwitter20-01-01.zip | head -n1 | python3 -m json.tool | vim -
```

You will follow the [MapReduce](https://en.wikipedia.org/wiki/MapReduce) procedure to analyze these tweets.
MapReduce is a famous procedure for large scale parallel processing that is widely used in industry.
It is a 3 step procedure summarized in the following image:

<img src=mapreduce.png width=100% />

I have already done the partition step for you (by splitting up the tweets into one file per day).
You will have to do the map and reduce steps.

**Runtime:**

The simplest and most common scenario is that the map procedure takes time O(n) and the reduce procedure takes time O(1).
If you have p<<n processors, then the overall runtime will be O(n/p).
This means that:
1. doubling the amount of data will cause the analysis to take twice as long;
1. doubling the number of processors will cause the analysis to take half as long;
1. if you want to add more data and keep the processing time the same, then you need to add a proportional number of processors.

More complex runtimes are possible.
Merge sort over MapReduce is the classic example. 
Here, mapping is equivalent to sorting and so takes time O(n log n),
and reducing is a call to the `_reduce` function that takes time O(n).
But they are both rare in practice and require careful math to describe,
so we will ignore them.
In the merge sort example, it requires p=n processors just to reduce the runtime down to O(n)...
that's a lot of additional computing power for very little gain,
and so is impractical.


## Tasks

Complete the following tasks:

1. Modify the `map.py` file so that it tracks the usage of the hashtags on both a language and country level.
   This will require creating a variable `counter_country` similar to the variable `counter_lang`, 
   and modifying this variable in the `#search hashtags` section of the code appropriately.
   The output of running `map.py` should be two files now, one that ends in `.lang` for the lanuage dictionary (same as before),
   and one that ends in `.country` for the country dictionary.

   **HINT:**
   Most tweets contain a `place` key,
   which contains a dictionary with the `country_code` key.
   This is how you should lookup the country that a tweet was sent from.
   Some tweets, however, do not have a `country_code` key.
   This can happen, for example, if the tweet was sent from international waters or the [international space station](https://unistellaroptics.com/10-years-ago-today-the-first-tweet-was-sent-directly-from-space/).
   Your code will have to be generic enough to handle edge cases similar to this without failing.

2. Once your `map.py` file has been modified to track results for each country,
   you should run the map file on all the tweets in the `/data-fast/twitter\ 2020` folder.
   In order to do this, you should create a shell script `run_maps.sh` that loops over each file in the dataset and runs `map.py` on that file.
   Each call to `map.py` can take between minutes to hours to finish.
   (The exact runtime will depend on the server's load due to other students.)
   So you should use the `nohup` command to ensure the program continues to run after you disconnect and the `&` operator to ensure that all `map.py` commands run in parallel.

3. After your modified `map.py` has run on all the files,
   you should have a large number of files in your `outputs` folder.
   Use the `reduce.py` file to combine all of the `.lang` files into a single file,
   and all of the `.country` files into a different file.
   Then use the `visualize.py` file to count the total number of occurrences of each of the hashtags.

   For each hashtag, you should create an output file in your repo using output redirection
   ```
   $ ./src/visualize.py --input_path=PATH --key=HASHTAG | head > viz/HASHTAG
   ```
   but replace `PATH` with the path to the output of your `reduce.py` file and `HASHTAG` is replaced with the hashtag you are analyzing.

4. Commit all of your code and visualization output files to your github repo and push the results to github.


## Results

After analyzing all geotagged tweets sent in 2020 using the process of Mapping, Reducing, and Visualizing, I created four differnet plots to represent certain relationships. The bar charts show how often a specific hashtag is used in tweets in 2020 sorted by the top ten countries/languages. 


This plot represents the number of tweets with the hashtag #코로나바이러스 by language. As you can see the most tweets using this hashtag are found in Korean and English. This hashtag is in the language Korean (meaning Coronavirus) and thus it makes sense that it is most commonly found in Korean tweets.

![reduced lang#코로나바이러스](https://user-images.githubusercontent.com/72474086/223543279-a33f79e6-d969-4a15-8cfe-4e4d708655e6.png)


This plot represents the number of tweets with the hashtag #coronavirus by language. As you can see the languages English and Spanish have the most tweets using the hashtag #coronavirus. Being that it is an english word, it makes sense that the hashtag is found significantly more in English tweets than any other language.

![reduced lang#coronavirus](https://user-images.githubusercontent.com/72474086/223544491-321813a9-5bde-4b99-9f36-fe6af300e267.png)


This plot represents the number of tweets with the hashtag #코로나바이러스 by country. #코로나바이러스 is found significantly more in Korea than any other country. There are very few tweets using this hashtag outside of Korea.

![reduced country#코로나바이러스](https://user-images.githubusercontent.com/72474086/223545156-854ace8f-bc22-4ff4-9689-4847cc607b67.png)


This plot represents the number of tweets with the hashtag #coronavirus by country. The tweets using this hastag are mostly found in the United States and other English speaking countries.

![reduced country#coronavirus](https://user-images.githubusercontent.com/72474086/223545579-9e9f0c0c-e518-4d7a-8950-3770704065cc.png)
