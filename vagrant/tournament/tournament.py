#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class Tournament(object):
    def __init__(self, tournament=None):
        """The constructor opens a connection to the database and starts a tournament. The parameter tournament accepts
         a tournament name. If a tournament by that name exists it will be used for this instance, if not, a new tournament
         is created with that name.
        """
        self.conn = None
        self.cur = None
        self._connect()
        self.rounds = 0

        self.tournId = self._getTournament(tournament)

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def _connect(self):
        """Connect to the PostgreSQL database.  Returns a database connection."""
        self.conn = psycopg2.connect("dbname=tournament user=postgres password=test")
        self.cur = self.conn.cursor()

    def _getTournament(self, tname):
        """Gets or creates a tournament by the name tname.

        Returns:
            Id of the tournament created or retrieved.
        """
        tid = None

        if tname:
            self.cur.execute("SELECT id FROM tournaments where name like %s", (tname,))
            tid = self.cur.fetchone()

        if not tid:
            self.cur.execute("INSERT INTO tournaments (name) VALUES(%s) RETURNING id", (tname,))
            tid = self.cur.fetchone()
            self.conn.commit()

        return tid[0]

    def _haveMatched(self, id1, id2, matches):
        """Determine whether id1 and id2 have been paired matches.
        matches is a list of 2-tuples.

        Returns:
            True if the IDs have been paired, False if not.
        """
        for m in matches:
            if id1 in m and id2 in m:
                return True

        return False

    def startNewTournament(self, name=None):
        """Create a new tournament and assign its reference number to the this instance's tournament identifier tournId.

        Returns:
            The ID of the tournament created.
        """
        self.tournId = self._getTournament(name)
        return self.tournId

    def deleteTournamnets(self):
        """Remove all the tuornament records from the database."""
        self.cur.execute("DELETE FROM tournaments;")
        self.conn.commit()


    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.cur.execute("DELETE FROM matches;")
        self.conn.commit()


    def deletePlayers(self):
        """Remove all the player records from the database."""
        self.cur.execute("DELETE FROM players;")
        self.conn.commit()

    def countPlayers(self):
        """Returns the number of players currently registered."""
        self.cur.execute("SELECT count(*) FROM players;")
        r = self.cur.fetchone()
        return r[0]

    def countPlayersThisTourn(self):
        """Returns the number of players currently enrolled in this tournament."""
        self.cur.execute("SELECT count(*) FROM players where tournId = %s;", (self.tournId,))
        r = self.cur.fetchone()
        return r[0]


    def registerPlayer(self, name):
        """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)

        Args:
          name: the player's full name (need not be unique).
        """
        self.cur.execute("INSERT INTO PLAYERS (name, tournId) VALUES(%s, %s)", (name, self.tournId))
        self.conn.commit()

    def playerStandings(self):
        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place, or a player
        tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        self.cur.execute("SELECT id, name, wins, matches FROM player_standings WHERE tournId = %s", (self.tournId,))
        return self.cur.fetchall()


    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
          winner:  the id number of the player who won
          loser:  the id number of the player who lost
        """
        self.cur.execute("INSERT INTO MATCHES (tournId, winner, loser) VALUES(%s, %s, %s)", (self.tournId, winner, loser))
        self.conn.commit()

    def getMatches(self):
        """Returns player id pairs for all matches currently recorded.

        Returns:
            A list of tuples, each of which contains (id, winner, loser)
        """
        self.cur.execute("SELECT winner, loser FROM matches WHERE tournId = %s", (self.tournId,))
        return self.cur.fetchall()

    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal win record, that is, a player adjacent
        to him or her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        matches = self.getMatches()
        standings = self.playerStandings()
        paired = set()
        pairings = []

        for i in range(0, len(standings) - 1, 2):

            k = 1
            while True:
                p1 = standings[i]
                p2 = standings[i + 1]

                if self._haveMatched(p1[0], p2[0], matches):
                    s1 = standings[i + 1]
                    standings[i + 1] = standings[i + 1 + k]
                    standings[i + 1 + k] = s1
                    k += 1
                else:
                    break

            paired.add(p1[0])
            paired.add(p2[0])
            pairings.append((p1[0], p1[1], p2[0], p2[1]))

        return pairings

