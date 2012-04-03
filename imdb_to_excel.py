#MrScruff360@gmail.com
#http://pastebin.com/LgztTeTR


# A:Drive/Path
# B:Title
# C:Year
# D:Resolution
# E:Format?, Bluray,HDDVD,HDTV 

import json
import urllib
import os
import cStringIO
import csv

class imdb_to_csv():
    def __init__(self):
        self.movie_list = None
        self.file_obj = cStringIO.StringIO()

        self.file_obj = open('output.csv', 'wb')
        #self.field_names = ["Drive", "Year", "Resolution", "Format",
#                            "Plot", "Votes", "Rated", "Response", "Title", 
 #                           "Poster", "Writer", "ID", "Director", "Released", 
  #                          "Actors", "Genre", "Runtime", "Rating"]

        #self.field_names = {"Drive","Year"}

        self.csv_obj = csv.writer(self.file_obj, dialect='excel', delimiter=' ')


    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

    def parse_and_lookup(self):
        # ['R:', 'Blood', 'Simple', '1984']
        #['R:', 'Blood', 'The', 'Last', 'Vampire', '2009']
        #['R:', 'Blow', '2001']
        

            
        for line in self.movie_list:
            p_line = line.strip().split()
            
            drive = p_line[0] 
            year  = p_line[-1]
            title = ' '.join(map(str, p_line[1:-1]))
            
            print "Title: %s, Year: %s, Drive: %s" % (title, year, drive)
            
            s = self.lookup(title, year)
               
            #[u'Plot', u'Votes', u'Rated', u'Response', 
            #u'Title', u'Poster', u'Writer', u'ID', u'Director', 
            #u'Released', u'Actors', u'Year', u'Genre', u'Runtime', u'Rating']

            
            
            if s:
                self.parse_stats(s)
                

                


    def parse_stats(self, stats):

        utf_stats = []

        for v in stats.values():
            utf_stats.append(v.encode('utf-8'))

        if stats:            
            self.csv_obj.writerow(utf_stats)
         


    def lookup(self, title, year):
        response = urllib.urlopen("http://www.imdbapi.com/?t=%s&y=%s" % (title, year))
        stats = json.load(response)
    
        if stats:
            return stats
        else:
            return False


    def load_list(self, location):
        if os.path.exists(location):
            
            with open(location, "r") as tmp:
                self.movie_list = tmp.readlines()
                
            print "List loaded"
            return True
        
        else:
            print "Location does not exist: %s" % location
            return False
            

c = imdb_to_csv()
c.load_list("ml")
c.parse_and_lookup()
