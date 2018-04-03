CREATE TABLE "raw_tweets" (
	"id" serial NOT NULL,
	"tweetid" integer NOT NULL,
	"userid" integer NOT NULL,
	"date" TIMESTAMP NOT NULL,
	"message" TEXT NOT NULL,
	"username" TEXT NOT NULL,
	"lat" FLOAT,
	"lng" FLOAT,
	"language" varchar(10),
	CONSTRAINT raw_tweets_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "filtered_tweets" (
	"id" serial NOT NULL,
	"tweetid" integer NOT NULL,
	"userid" integer NOT NULL,
	"date" TIMESTAMP NOT NULL,
	"message" TEXT NOT NULL,
	"username" TEXT NOT NULL,
	"lat" FLOAT,
	"lng" FLOAT,
	"language" varchar(10),
	CONSTRAINT filtered_tweets_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "tweet_features" (
	"id" serial NOT NULL,
	"message" serial NOT NULL,
	"cntyid" serial NOT NULL,
	"weekid" serial(1) NOT NULL,
	"message_tkns" bytea NOT NULL,
	"message_filt_tkns" bytea NOT NULL,
	"topic" integer NOT NULL,
	"infer_lang" varchar(2) NOT NULL,
	"positive" FLOAT NOT NULL,
	"neutral" FLOAT NOT NULL,
	"negative" FLOAT NOT NULL,
	CONSTRAINT tweet_features_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "counties" (
	"countyid" integer NOT NULL,
	"geometry" bytea NOT NULL,
	"state" varchar(2) NOT NULL,
	CONSTRAINT counties_pk PRIMARY KEY ("countyid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "weeks" (
	"weekid" integer NOT NULL,
	"min_date" TIMESTAMP NOT NULL UNIQUE,
	"max_date" TIMESTAMP NOT NULL UNIQUE,
	CONSTRAINT weeks_pk PRIMARY KEY ("weekid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "topics" (
	"topicid" serial NOT NULL,
	"categories" bytea NOT NULL UNIQUE,
	CONSTRAINT topics_pk PRIMARY KEY ("topicid")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "filtered_tweets" ADD CONSTRAINT "filtered_tweets_fk0" FOREIGN KEY ("id") REFERENCES "raw_tweets"("id");

ALTER TABLE "tweet_features" ADD CONSTRAINT "tweet_features_fk0" FOREIGN KEY ("id") REFERENCES "filtered_tweets"("id");
ALTER TABLE "tweet_features" ADD CONSTRAINT "tweet_features_fk1" FOREIGN KEY ("message") REFERENCES "filtered_tweets"("message");
ALTER TABLE "tweet_features" ADD CONSTRAINT "tweet_features_fk2" FOREIGN KEY ("cntyid") REFERENCES "counties"("countyid");
ALTER TABLE "tweet_features" ADD CONSTRAINT "tweet_features_fk3" FOREIGN KEY ("weekid") REFERENCES "weeks"("weekid");
ALTER TABLE "tweet_features" ADD CONSTRAINT "tweet_features_fk4" FOREIGN KEY ("topic") REFERENCES "topics"("topicid");




