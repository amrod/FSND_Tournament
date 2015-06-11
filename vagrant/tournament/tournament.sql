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

CREATE VIEW player_wins as
select players.pid as id, count(winner)
from players left outer join matches
on (players.pid = matches.winner)
group by players.pid
order by count desc;



CREATE VIEW player_matches as
select players.pid as id, players.name as name, count(players.pid) as matches
from players, matches
where players.pid = matches.winner OR players.pid = matches.loser
group by players.pid;



CREATE VIEW player_standings as
select
    p.pid,
    p.name,
    (case when w.count is null then 0 else w.count end) as wins,
    (case when pm.matches is null then 0 else pm.matches end) as matches
from
    player_wins w LEFT OUTER JOIN player_matches pm ON (pm.id = w.id)
    JOIN players p on p.pid = w.id

order by wins desc;

