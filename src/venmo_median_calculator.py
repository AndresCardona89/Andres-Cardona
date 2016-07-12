#!/usr/bin/env python

import json
import datetime as dt
import statistics
import os


class PaymentEntry:
    """Class that represents each new entry.

    It takes a string with the JSON entry and decodes it to obtain its
    atrribuites.
    
    Attribuites:
        Text     String line from the input txt
        JSON     Dictionary with the decoded JSON info
        Actor    Decoded name of the 'actor' field
        Target   Decoded name of the 'target' field
        Time     Decoded time of the entry
        Valid    Helps identify if the entry was valid
    """

    TimeFormat = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, TextLine):
        # Class initialization
        # Takes one string argument containing a JSON payment and decodes it
        # to obtain its properties
        self.Text = TextLine
        self.Valid = False
        try:  # Try to decode the JSON entry
            self.JSon = json.loads(self.Text)  # Decodes JSON into dictionary
            self.Actor = self.JSon['actor']
            self.Target = self.JSon['target']
            self.Time = self.JSon['created_time']

            if '' not in [self.Time, self.Actor, self.Target]:
                # Checks for empty entries
                self.Time = dt.datetime.strptime(self.Time, self.TimeFormat)
                self.Valid = True  # Marks the enty as valid
        except:  # If decoding the JSON fails:
            pass


class Graph:
    """Class that represents the graph. It takes a new entry and updates its 
    arguments

    Attribuites:
        Nodes    List with the users that represent each node
        Edges    List with the list of connections/edges for each node
        Entries  List of PaymentEntry objects that fall withinin the timeframe
        Time     The time of the current graph. Defined as the latest entry

    It considers the entries that fall under within 60 seconds of the latest
    entry
    """

    def __init__(self):
        # Class initialization.

        self.Nodes = []
        self.Edges = []
        self.Entries = []
        self.Time = dt.datetime(1, 1, 1)

    def NewEntry(self, Entry):
        # This function takes one payment entry.
        # Arguments: PaymentEntry object

        # It updates its attribuites and constructs the graph according to
        # entries that should be represented in the graph

        # Reset graph attribuites
        self.Nodes = []
        self.Edges = []
        self.Entries.append(Entry)

        # Sets the new current time if necesary
        if self.Time < Entry.Time:
            self.Time = Entry.Time

        # Check the time of each entry in the list and deletes those that do
        # not fall under the 60 seconds window
        Indexes = []
        for In, EachEntry in enumerate(self.Entries):
            if (self.Time - EachEntry.Time).total_seconds() > 60:
                Indexes.append(In)  # Get indexes of entries to delete
        for n in sorted(Indexes, reverse=True):
            self.Entries.pop(n)  # Delete entries

        for EachEntry in self.Entries:
            # With the new entries list it reconstructs the graph

            # Add new nodes if necesary
            if EachEntry.Actor not in self.Nodes:
                self.Nodes.append(EachEntry.Actor)  # Add new node with actor
                self.Edges.append([])  # Add the node's edges
            if EachEntry.Target not in self.Nodes:
                self.Nodes.append(EachEntry.Target)  # Add new node with target
                self.Edges.append([])  # Add the node's edges

            # Find the actor's node index to update its edges in list
            NodeIndex = self.Nodes.index(EachEntry.Actor)
            if EachEntry.Target not in self.Edges[NodeIndex]:
                # Make sure that no repited edges are included
                self.Edges[NodeIndex].append(EachEntry.Target)

            # Find the target's node index to update its edges in list
            NodeIndex = self.Nodes.index(EachEntry.Target)
            if EachEntry.Actor not in self.Edges[NodeIndex]:
                # Make sure that no repited edges are included
                self.Edges[NodeIndex].append(EachEntry.Actor)


class MedianTXTCreator:
    """This class calculates the median for every new entry and writes to the
    txt ouput file.

    Attribuites:
        Edges        Input argument with the edges of each node in the graph
        EdgesNumber  List with the number of edges for each node
        Median       Median of the current graph
    """

    def __init__(self):
        self.Edges = []
        self.EdgesNumber = []
        self.Median = 0.00

    def NewEntry(self, Edges):
        #It recalculates and writes a new median for every new list of edges
        # Arguments: list of list with the edges of each node
        self.EdgesNumber = []

        # Calculate number of edges for each node
        for EachEdge in Edges:
            self.EdgesNumber.append(len(EachEdge))

        # Calculate mediean and make sure it has 2 decimal digits
        self.Median = float(statistics.median(sorted(self.EdgesNumber)))

        global OutTXT
        OutTXT.write(str("%.2f" % self.Median + '\n'))  # Write to txt file


def main():
    CurrentDir = os.path.abspath(__file__ + "/../../")
    VenmoFile = open(CurrentDir + '/venmo_input/venmo-trans.txt', 'r')
    VenmoLines = VenmoFile.readlines()  # Read the JSON lines from the file
    VenmoFile.close()  # Close file to free memory
    EntriesList = []

    global CurrentGraph
    global txtCreator
    global OutTXT

    CurrentGraph = Graph()
    txtCreator = MedianTXTCreator()
    OutTXT = open(CurrentDir + '/venmo_output/output.txt', 'w')

    for LineNumber in range(len(VenmoLines)):
        # Goes through each JSON line and creates one PaymentEntry object for
        # each entry.
        EntriesList.append(PaymentEntry(VenmoLines[LineNumber]))
        if EntriesList[-1].Valid:
            # Verifies the entry. If entry is not proper it skips the graph
            # update
            CurrentGraph.NewEntry(EntriesList[-1])  # Calls graph update
            txtCreator.NewEntry(CurrentGraph.Edges)  # Recalculate median

    OutTXT.close()

main()
