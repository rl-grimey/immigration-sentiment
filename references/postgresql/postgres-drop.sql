ALTER TABLE "filtered_tweets" DROP CONSTRAINT IF EXISTS "filtered_tweets_fk0";

ALTER TABLE "tweet_features" DROP CONSTRAINT IF EXISTS "tweet_features_fk0";

ALTER TABLE "tweet_features" DROP CONSTRAINT IF EXISTS "tweet_features_fk1";

ALTER TABLE "tweet_features" DROP CONSTRAINT IF EXISTS "tweet_features_fk2";

ALTER TABLE "tweet_features" DROP CONSTRAINT IF EXISTS "tweet_features_fk3";

ALTER TABLE "tweet_features" DROP CONSTRAINT IF EXISTS "tweet_features_fk4";

DROP TABLE IF EXISTS "raw_tweets";

DROP TABLE IF EXISTS "filtered_tweets";

DROP TABLE IF EXISTS "tweet_features";

DROP TABLE IF EXISTS "counties";

DROP TABLE IF EXISTS "weeks";

DROP TABLE IF EXISTS "topics";
