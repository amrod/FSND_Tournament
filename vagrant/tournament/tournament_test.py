#!/usr/bin/env python
#
# Test cases for tournament.py
import unittest
from tournament import Tournament


class TestTournament(unittest.TestCase):

    def setUp(self):
        self.t = Tournament()
        self.t.deleteMatches()
        self.t.deletePlayers()

    def tearDown(self):
        self.t.deleteMatches()
        self.t.deletePlayers()
        del self.t

    def test_DeleteMatches(self):
        self.t.deleteMatches()
        print "1. Old matches can be deleted."


    def testDelete(self):

        print "2. Player records can be deleted."


    def testCount(self):
        c = self.t.countPlayers()
        if c == '0':
            raise TypeError(
                "countPlayers() should return numeric zero, not string '0'.")
        if c != 0:
            raise ValueError("After deleting, countPlayers should return zero.")
        print "3. After deleting, countPlayers() returns zero."


    def testRegister(self):
        self.t.registerPlayer("Chandra Nalaar")
        c = self.t.countPlayers()
        if c != 1:
            raise ValueError(
                "After one player registers, countPlayers() should be 1.")
        print "4. After registering a player, countPlayers() returns 1."


    def testRegisterCountDelete(self):
        self.t.registerPlayer("Markov Chaney")
        self.t.registerPlayer("Joe Malik")
        self.t.registerPlayer("Mao Tsu-hsi")
        self.t.registerPlayer("Atlanta Hope")
        c = self.t.countPlayers()
        if c != 4:
            raise ValueError(
                "After registering four players, countPlayers should be 4.")
        self.t.deletePlayers()
        c = self.t.countPlayers()
        if c != 0:
            raise ValueError("After deleting, countPlayers should return zero.")
        print "5. Players can be registered and deleted."


    def testStandingsBeforeMatches(self):
        self.t.registerPlayer("Melpomene Murray")
        self.t.registerPlayer("Randy Schwartz")
        standings = self.t.playerStandings()
        if len(standings) < 2:
            raise ValueError("Players should appear in playerStandings even before "
                             "they have played any matches.")
        elif len(standings) > 2:
            raise ValueError("Only registered players should appear in standings.")
        if len(standings[0]) != 4:
            raise ValueError("Each playerStandings row should have four columns.")
        [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
        if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
            raise ValueError(
                "Newly registered players should have no matches or wins.")
        if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
            raise ValueError("Registered players' names should appear in standings, "
                             "even if they have no matches played.")
        print "6. Newly registered players appear in the standings with no matches."


    def testReportMatches(self):
        self.t.registerPlayer("Bruno Walton")
        self.t.registerPlayer("Boots O'Neal")
        self.t.registerPlayer("Cathy Burton")
        self.t.registerPlayer("Diane Grant")
        standings = self.t.playerStandings()
        [id1, id2, id3, id4] = [row[0] for row in standings]
        self.t.reportMatch(id1, id2)
        self.t.reportMatch(id3, id4)
        standings = self.t.playerStandings()
        for (i, n, w, m) in standings:
            if m != 1:
                raise ValueError("Each player should have one match recorded.")
            if i in (id1, id3) and w != 1:
                raise ValueError("Each match winner should have one win recorded.")
            elif i in (id2, id4) and w != 0:
                raise ValueError("Each match loser should have zero wins recorded.")
        print "7. After a match, players have updated standings."


    def testPairings(self):
        self.t.deleteMatches()
        self.t.deletePlayers()
        self.t.registerPlayer("Twilight Sparkle")
        self.t.registerPlayer("Fluttershy")
        self.t.registerPlayer("Applejack")
        self.t.registerPlayer("Pinkie Pie")
        standings = self.t.playerStandings()
        [id1, id2, id3, id4] = [row[0] for row in standings]
        self.t.reportMatch(id1, id2)
        self.t.reportMatch(id3, id4)
        pairings = self.t.swissPairings()
        if len(pairings) != 2:
            raise ValueError(
                "For four players, swissPairings should return two pairs.")
        [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
        correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
        actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
        if correct_pairs != actual_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
        print "8. After one match, players with one win are paired."

    def testHaveMathced(self):
        self.t.registerPlayer("Player 1")
        self.t.registerPlayer("Player 2")
        self.t.registerPlayer("Player 3")
        self.t.registerPlayer("Player 4")

        standings = self.t.playerStandings()
        [id1, id2, id3, id4] = [row[0] for row in standings]

        self.t.reportMatch(id1, id2)
        self.t.reportMatch(id4, id3)

        matches = self.t.getMatches()

        self.assertTrue(self.t._haveMatched(id1, id2, matches))
        self.assertTrue(self.t._haveMatched(id2, id1, matches))
        self.assertTrue(self.t._haveMatched(id3, id4, matches))
        self.assertFalse(self.t._haveMatched(id1, id3, matches))
        self.assertFalse(self.t._haveMatched(id3, id1, matches))

    def testNoRematches(self):
        self.t.registerPlayer("Player 1")
        self.t.registerPlayer("Player 2")
        self.t.registerPlayer("Player 3")
        self.t.registerPlayer("Player 4")
        self.t.registerPlayer("Player 5")
        self.t.registerPlayer("Player 6")
        self.t.registerPlayer("Player 7")
        self.t.registerPlayer("Player 8")
        self.t.registerPlayer("Player 9")
        self.t.registerPlayer("Player 10")
        self.t.registerPlayer("Player 11")
        self.t.registerPlayer("Player 12")

        standings = self.t.playerStandings()
        [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10, id11, id12] = [row[0] for row in standings]
        # Round 1
        self.t.reportMatch(id1, id2)
        self.t.reportMatch(id4, id3)
        self.t.reportMatch(id5, id6)
        self.t.reportMatch(id7, id8)
        self.t.reportMatch(id9, id10)
        self.t.reportMatch(id12, id11)
        # Round 2
        self.t.reportMatch(id4, id1)
        self.t.reportMatch(id5, id7)
        self.t.reportMatch(id9, id12)
        self.t.reportMatch(id3, id2)
        self.t.reportMatch(id6, id8)
        self.t.reportMatch(id11, id10)
        # Round 3
        self.t.reportMatch(id4, id5)
        self.t.reportMatch(id9, id1)
        self.t.reportMatch(id7, id11)
        self.t.reportMatch(id3, id12)
        self.t.reportMatch(id2, id6)
        self.t.reportMatch(id10, id8)

        pairings = self.t.swissPairings()
        # print "Pairings:"
        # for p in pairings:
        #     print p
        self.assertFalse((id6, 'Player 6', id10, 'Player 10') in pairings)

if __name__ == '__main__':
    unittest.main()