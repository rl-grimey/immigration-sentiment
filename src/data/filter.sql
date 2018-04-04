INSERT INTO filter_tweets 
SELECT DISTINCT ON ("tweetID") * 
FROM   raw_tweets 
WHERE  ( message IS NOT NULL ) 
       AND ( retweet IS NULL ) 
       AND ( LEFT(language, 2) ILIKE 'en' ) 
       AND ( latitude IS NOT NULL )
       AND ( longitude IS NOT NULL )
       AND ( DATE >= '2016-12-30 00:00:00' 
           AND DATE < '2017-02-25 00:00:00' ) ;
