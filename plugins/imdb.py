import re
import urllib2

from lxml.html import parse

asciionly = re.compile(r'[^a-zA-Z]')

class imdblib(object):
    class Movie(object):
        def __init__(self, id, fullplot = False):
            if isinstance(id, int):
                id = str(id)
            m = re.search(r'(?:tt)?(?P<id>\d{7})', id, re.I)
            if m:
                self.id = m.group('id')
            else:
                raise ValueError('Invalid imdb id.')
    
            self.title = None
            self.genres = []
            self.rating = None
            self.votes = None
            self.top = None
            self.directors = []
            self.plot = None
            self.fullplot = None
            self.tagline = None
            self.release = None
            self.runtime = None
            self.countries = []
            self.languages = []
            self.cast = []
            self.year = None
            self.usercomment = None
            self.posterurl = None
            self.fullplot = fullplot
            self.update()
    
    
        def _infodiv(self, title, find=None):
            try:
                if not find:
                    return self.infodivs[title].text.replace('\n', '').strip()
                else:
                    return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                    
            except:
                if not find:
                    return None
                else:
                    return []
    
    
        def update(self):
            data = urllib2.urlopen('http://www.imdb.com/title/tt%s/' % self.id)
            movie = parse(data).getroot()
    
            self.infodivs = {}
            for e in movie.cssselect('#tn15content div.info'):
                title = e.find('h5')
                content = e.find('div')
                if title is not None and title.text is not None and content is not None:
                    self.infodivs[asciionly.sub('', title.text).lower()] = content
            for old, new in (('writer', 'writers'), ('director', 'directors')):
                if old in self.infodivs:
                    self.infodivs[new] = self.infodivs[old]
    
            try:
                self.title = movie.find('head').find('title').text
            except:
                self.title = 'Unknown title'
    
            year = re.search(r'\((?P<year>\d{4})\)$', self.title)
            if year:
                self.year = year.group('year')
                self.title = re.sub(r'\s\(\d{4}\)$', '', self.title)
            
            if 'directors' in self.infodivs:
                self.directors = [x.text for x in self.infodivs['directors'].findall('.//a')]
            
            if 'genre' in self.infodivs:
                self.genres = [x.text for x in self.infodivs['genre'].findall('.//a') if '/Sections' in x.attrib.get('href')]
            try:
                rating = html.get_element_by_id('tn15rating')
                if rating is not None:
                    self.rating = rating.cssselect('div .meta b')[0].text
                    self.votes = rating.cssselect('div .meta a')[0].text
                    top = rating.cssselect('div .bottom a')
                    if top:
                        self.top = top[0].text
            except:
                self.rating = None
                self.votes = 'No votes'
                self.top = None
            
    
            self.plot = self._infodiv('plot')
            self.tagline = self._infodiv('tagline')
            self.release = self._infodiv('releasedate')
            self.usercomment = self._infodiv('usercomments')
            self.runtime = self._infodiv('runtime')
            self.countries = self._infodiv('country', find='a')
            self.languages = self._infodiv('language', find='a')
            self.cast = []
            for x in movie.cssselect('table.cast tr'):
                name = x.cssselect('.nm a') or x.cssselect('.nm')
                if name:
                    name = name[0].text.strip()
                
                character = x.cssselect('.char a') or x.cssselect('.char')
                if character:
                    character = character[0].text.strip()
    
                if name and character:
                    self.cast.append((name, character))
            
            try:
                self.posterurl = movie.cssselect('div.photo img')[0].get('src')
                if 'title_addposter' in self.posterurl:
                    self.posterurl = None
            except (TypeError, KeyError):
                self.posterurl = None
    
            if self.fullplot:            
                data = urllib2.urlopen("http://www.imdb.com/title/tt%s/plotsummary" % self.id)
                movie = parse(data).getroot()
                try:
                    self.fullplot = movie.cssselect('p.plotpar')[0].text.strip()
                except AttributeError:
                    pass    
    
    class Name(object):
        def __init__(self, id):
            if isinstance(id, int):
                id = str(id)
            m = re.search(r"(?:nm)?(?P<id>\d{7})", id, re.I)
            if m:
                self.id = m.group("id")
            else:
                raise ValueError("Invalid imdb id.")
    
            self.name = None
            self.birthdate = None
            self.birthplace = None
            self.deathdate = None
            self.biography = None
            self.trivia = None
            self.awards = None
            self.altnames = None
            self.filmography = []
            self.photourl = None
            self.update()
    
    
        def _infodiv(self, title, find=None):
            try:
                if not find:
                    return self.infodivs[title].text.replace('\n', '').strip()
                else:
                    return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                    
            except:
                if not find:
                    return None
                else:
                    return []
    
    
        def update(self):
            data = urllib2.urlopen('http://www.imdb.com/name/nm%s/' % self.id)
            movie = parse(data).getroot()
    
            self.infodivs = {}
            for e in movie.cssselect('#tn15content div.info'):
                title = e.find('h5')
                content = e.find('div')
                if title is not None and title.text is not None and content is not None:
                    self.infodivs[asciionly.sub('', title.text).lower()] = content
            for old, new in (('writer', 'writers'), ('director', 'directors')):
                if old in self.infodivs:
                    self.infodivs[new] = self.infodivs[old]
    
            try:
                self.name = movie.find('head').find('title').text
            except:
                self.name = 'Unknown name'
                
            self.birthdate = ' '.join(self._infodiv('dateofbirth', find='a')[:2])
            try:
                self.birthplace = self._infodiv('dateofbirth', find='a')[2]
            except Exception:
                pass
            self.deathdate = ' '.join(self._infodiv('dateofdeath', find='a')[:2])
            self.biography = self._infodiv('minibiography')
            self.trivia = self._infodiv('trivia')
            self.awards = self._infodiv('awards')
            if self.awards:
                self.awards = re.sub(r'\s+', ' ', self.awards.strip())
            self.altnames = self._infodiv('alternatenames')
     
            try:
                self.photourl =  movie.cssselect('div.photo img')[0].get('src')
                if "nophoto" in self.photourl:
                    self.photourl = None
            except TypeError,KeyError:
                self.photourl = None
    
            data = urllib2.urlopen('http://www.imdb.com/name/nm%s/filmorate' % self.id)
            movie = parse(data).getroot()
    
            self.filmography = [x.text for x in movie.cssselect('.filmo li > a')]
    
    
    class Search:
        def __init__(self, string, name=False):
            self.searchstring = string
            self.result = None
            self.name = name
            self.update()
    
        def update(self, searchstring = None):
            if not searchstring:
                searchstring = self.searchstring
            else:
                self.searchstring = searchstring
           
            m = re.search(r"(?P<result>(?:nm|tt)\d{7})", searchstring, re.I)
            if m:
                self.result = m.group("result")
                return
            
            if self.name:
                regex = [r"<a href=\"\/name\/(nm\d{7})\/\"[^>]*>([^<]*?)</a>"]
                url = "http://www.imdb.com/find?s=nm&q=%s" % urllib2.quote(searchstring.encode('latin-1'))
            else:
                m = re.search(r"(?P<movie>.+?)(?: \(?(?P<year>\d{4})\)?)?$", searchstring, re.I)
                movie = m.group("movie").strip(" ")
                year = m.group("year")
                movie = re.escape(movie)
        
                regex = []
                if year:
                   year = re.escape(year)
                   regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+")</a> \("+year+"\)")
                   regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+", The)</a> \("+year+"\)")
                   regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>(\""+movie+"\")</a> \("+year+"\)")
                   regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?"+movie+"[^<]*?)</a> \("+year+"\)")
                   regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?)</a> \("+year+"\)")
                regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+")</a>")
                regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+", The)</a>")
                regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>(\""+movie+"\")</a>")
                regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?"+movie+"[^<]*?)</a>")
                regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?)</a>")
                url = "http://www.imdb.com/find?s=tt&q=%s" % urllib2.quote(m.group("movie").encode('latin-1'))
            
        
            url = urllib2.urlopen(url)
            if "/find?s=" not in url.url: # We've been redirected to the first result
                m = re.search(r"/(?:name|title)/(?P<result>(?:nm|tt)\d{7})", url.url, re.I)
                if m:
                    self.result = m.group("result")
                    return
                
            #data = _unescape(url.read())
            data = url.read()
    
            self.result = None
            for x in regex:
                m = re.search(x, data, re.IGNORECASE)
                if m:
                    self.result = m.group(1)
                    break
    
    def imdb(self, input):
        """Get information about a movie, tv show or actor."""
        cmd = input.args
        
        parser = self.OptionParser()
        parser.add_option("-r", "--rating", dest="rating", action="store_true", default=False)
        parser.add_option("-R", "--RATING", dest="rating_url", action="store_true", default=False)
        parser.add_option("-n", "-p", "--name", "--person", dest="person", action="store_true", default=False)
        (options, args) = parser.parse_args(cmd.split())
    
        if not args:
            raise self.BadInputError("A query is required.")
        
        query = " ".join(args)
        if options.person:
            try:
                id = imdblib.Search(query, name=True).result
                if id:
                    name = imdblib.Name(id)
                else:
                    self.say("Your search for \x02%s\x02 did not return any results." % query)
                    return
            except urllib2.HTTPError:
                self.say("Your search for \x02%s\x02 did not return any results." % query)
                return
            except IOError:
                self.say("Error: A connection to IMDB could not be established.")
                
            self.say("\x02%s\x02 - [ \x1f%s\x1f ]" % (name.name, "http://www.imdb.com/name/nm"+name.id))
            if name.birthdate or name.birthplace:
                self.say("\x02Born:\x02 %s" % (name.birthdate or "")+(name.birthplace and " in "+name.birthplace))
            if name.deathdate: self.say("\x02Died:\x02 %s" % name.deathdate)
            if name.biography: self.say("\x02Biography:\x02 %s" % name.biography)
            if name.trivia: self.say("\x02Trivia:\x02 %s" % name.trivia)
            if name.awards: self.say("\x02Awards:\x02 %s" % name.awards)
            if name.altnames: self.say("\x02Alternative names:\x02 %s" % name.altnames)
            if name.filmography: self.say("\x02Filmography:\x02 %s" % ", ".join(name.filmography[:5]))
    
        else:
            if options.rating or options.rating_url:
                queries = query.split(",")
            else:
                queries = [query]
            for query in queries:
                query = query.strip()
                try:
                    id = imdblib.Search(query)
                    if id.result:
                        movie = imdblib.Movie(id.result)
                    else:
                        self.say("Your search for \x02%s\x02 did not return any results." % query)
                        return
                except urllib2.HTTPError:
                    self.say("Your search for \x02%s\x02 did not return any results." % query)
                    return
                except IOError:
                    self.say("Error: A connection to IMDB could not be established.")
                
    
                if options.rating_url:
                    if movie.rating:
                        self.say("\x02%s%s\x02:  %s (%s) %s - [ \x1f%s\x1f ]" % (movie.title, movie.year and " ("+str(movie.year)+")" or "", movie.rating, movie.votes, movie.top and "["+movie.top+"]" or "", "http://www.imdb.com/title/tt"+movie.id))
                    else:
                        self.say("\x02%s%s\x02 is not yet rated. - [ \x1f%s\x1f ]" % (movie.title, movie.year and " ("+str(movie.year)+")" or "", "http://www.imdb.com/title/tt"+movie.id))
    
    
                elif options.rating:
                    if movie.rating:
                        self.say("\x02%s%s\x02:  %s (%s) %s" % (movie.title, movie.year and " ("+str(movie.year)+")" or "", movie.rating, movie.votes, movie.top and "["+movie.top+"]" or ""))
                    else:
                        self.say("\x02%s%s\x02 is not yet rated." % (movie.title, movie.year and " ("+str(movie.year)+")" or "",))
    
    
                else:
                    self.say("\x02%s%s\x02 - [ \x1f%s\x1f ]" % (movie.title, movie.year and " ("+str(movie.year)+")" or "", "http://www.imdb.com/title/tt"+movie.id))
                    if movie.directors: self.say("\x02Director:\x02 %s" % ", ".join(movie.directors))
                    if movie.genres: self.say("\x02Genre:\x02 %s" % ", ".join(movie.genres))
                    if movie.rating: self.say("\x02Rating:\x02 %s (%s) %s" % (movie.rating, movie.votes, movie.top and "["+movie.top+"]" or ""))
                    if movie.plot: self.say("\x02Plot:\x02 %s" % movie.plot)
                    if movie.tagline: self.say("\x02Tagline:\x02 %s" % movie.tagline)
                    if movie.release: self.say("\x02Release:\x02 %s" % movie.release)
                    if movie.runtime: self.say("\x02Runtime:\x02 %s" % movie.runtime)
                    if movie.countries: self.say("\x02Country:\x02 %s" % ", ".join(movie.countries))
                    if movie.languages: self.say("\x02Language:\x02 %s" % ", ".join(movie.languages))
                    if movie.usercomment: self.say("\x02User comments:\x02 %s" % movie.usercomment)
                    if movie.cast: self.say("\x02Cast:\x02 %s" % ", ".join([name+" as "+cname for name, cname in movie.cast[:5]]))

imdb.rule = ["mdb", "imdb"]
imdb.usage = [("Display information about a movie or tv show", "$pcmd <title>"),
    ("Display information about an actor", "$pcmd -p <name>"),
    ("Only show the title and rating for a list of movies", "$pcmd -r <title>[, <title>[, <title>...]]")]
imdb.example = [("Display information about the movie V for Vendetta", "$pcmd V for Vendetta"),
    ("Display information about the actor Rob McElhenney", "$pcmd -p Rob McElhenney"),
    ("Show the title and rating for the first three terminator movies", "$pcmd -r The Terminator, Terminator 2: Judgment Day, Terminator 3: Rise of the Machines")]