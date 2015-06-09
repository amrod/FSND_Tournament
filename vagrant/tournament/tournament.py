#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class Tournament(object):

    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        """Connect to the PostgreSQL database.  Returns a database connection."""
        self.conn = psycopg2.connect("dbname=tournament user=postgres password=test")
        self.cur = self.conn.cursor()
        return self.conn


    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.cur.execute("DELETE FROM matches;")


    def deletePlayers(self):
        """Remove all the player records from the database."""
        self.cur.execute("DELETE FROM players;")


    def countPlayers(self):
        """Returns the number of players currently registered."""
        self.cur.execute("SELECT count(*) FROM players;")
        r = self.cur.fetchone()
        return r[0]


    def registerPlayer(self, name):
        """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)

        Args:
          name: the player's full name (need not be unique).
        """
        self.cur.execute("INSERT INTO PLAYERS (name) VALUES('{}')".format(name))


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
        self.cur.execute("select * ")


    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
          winner:  the id number of the player who won
          loser:  the id number of the player who lost
        """
        self.cur.execute("INSERT INTO MATCHES VALUES('{}, {}')".format(winner, loser))



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


