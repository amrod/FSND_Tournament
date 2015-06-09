-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
    pid serial primary key,
    name varchar(32)
);

CREATE TABLE matches (
    id serial primary key,
    winner integer REFERENCES players (pid),
    loser integer REFERENCES players (pid)
);

CREATE VIEW WINS as
select winner as id, count(winner) from matches group by winner order by count desc;

CREATE VIEW LOSSES as
select loser as id, count(loser) from matches group by loser order by count desc;
