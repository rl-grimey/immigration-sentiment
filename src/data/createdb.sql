CREATE TABLE IF NOT EXISTS "raw_tweets" (
    "id" SERIAL NOT NULL,
    "tweetID" BIGINT NOT NULL,
    "date" TIMESTAMP,
    "message" TEXT,
    "username" TEXT,
    "userID" BIGINT NOT NULL,
    "language" VARCHAR(10),
    "longitude" FLOAT,
    "latitude" FLOAT,
    "retweet" TEXT,
    CONSTRAINT raw_tweets_pk PRIMARY KEY ("id")
) WITH ( OIDS=FALSE );
CREATE TABLE IF NOT EXISTS "filter_tweets" (
    "id" SERIAL NOT NULL,
    "tweetID" BIGINT NOT NULL,
    "date" TIMESTAMP,
    "message" TEXT,
    "username" TEXT,
    "userID" BIGINT NOT NULL,
    "language" VARCHAR(10),
    "longitude" FLOAT,
    "latitude" FLOAT,
    "retweet" TEXT
) WITH ( OIDS=FALSE );
ALTER TABLE "filter_tweets" ADD CONSTRAINT "filter_fk0" FOREIGN KEY ("id") REFERENCES "raw_tweets"("id");
