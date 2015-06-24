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
    id serial PRIMARY KEY,
    name VARCHAR(32)
);

CREATE TABLE tournaments (
    id serial PRIMARY KEY,
    name varchar(64)
);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    tournId INTEGER REFERENCES tournaments (id) ON DELETE CASCADE,
    winner INTEGER REFERENCES players (id),
    loser INTEGER REFERENCES players (id)
);

-- List total number of wins for player.
CREATE VIEW player_wins AS
SELECT players.id AS id, matches.tournId, COUNT(winner)
FROM players LEFT OUTER JOIN matches
ON (players.id = matches.winner)
GROUP BY players.id, matches.tournId
ORDER BY COUNT DESC;


-- List total number of matches each player has played.
CREATE VIEW player_matches AS
SELECT
    players.id AS id,
    players.name AS name,
    matches.tournId,
    COUNT(matches.id) AS matches
FROM players LEFT OUTER JOIN matches
ON (players.id = matches.winner OR players.id = matches.loser)
GROUP BY players.id, matches.tournId;

-- List total number of wins and matches for each player.
CREATE VIEW player_standings AS
SELECT
    p.id,
    p.name,
    pm.tournId,
    (CASE WHEN w.count IS NULL THEN 0 ELSE w.count END) AS wins,
    (CASE WHEN pm.matches IS NULL THEN 0 ELSE pm.matches END) AS matches
from
    player_wins w LEFT OUTER JOIN player_matches pm ON (pm.id = w.id)
    JOIN players p ON p.id = w.id
ORDER BY wins DESC, p.id ASC;
