INSERT INTO filter_tweets 
SELECT DISTINCT ON ("tweetID") * 
FROM   raw_tweets 
WHERE  ( message IS NOT NULL ) 
       AND ( retweet IS NULL ) 
       AND ( Left(LANGUAGE, 2) LIKE 'en' ) 
       AND ( latitude IS NOT NULL ) 
       AND ( DATE >= '2016-12-30 04:00:00' 
             AND DATE < '2017-02-24 04:00:00' ) 
       AND ( longitude IS NOT NULL );
