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
    pid serial PRIMARY KEY,
    name VARCHAR(32)
);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner INTEGER REFERENCES players (pid),
    loser INTEGER REFERENCES players (pid)
);

-- List total number of wins for player.
CREATE VIEW player_wins AS
SELECT players.pid AS id, COUNT(winner)
FROM players LEFT OUTER JOIN matches
ON (players.pid = matches.winner)
GROUP BY players.pid
ORDER BY COUNT DESC;


-- List total number of matches each player has played.
CREATE VIEW player_matches AS
SELECT
    players.pid AS id,
    players.name AS name,
    COUNT(matches.id) AS matches
FROM players LEFT OUTER JOIN matches
ON (players.pid = matches.winner OR players.pid = matches.loser)
GROUP BY players.pid;

-- List total numbers of win and matches for each player.
CREATE VIEW player_standings AS
SELECT
    p.pid,
    p.name,
    (CASE WHEN w.count IS NULL THEN 0 ELSE w.count END) AS wins,
    (CASE WHEN pm.matches IS NULL THEN 0 ELSE pm.matches END) AS matches
from
    player_wins w LEFT OUTER JOIN player_matches pm ON (pm.id = w.id)
    JOIN players p ON p.pid = w.id
ORDER BY wins DESC;

