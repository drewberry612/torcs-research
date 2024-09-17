class ServerState(object):
    '''
    What the server is reporting currently
    '''
    def __init__(self):
        self.servstr = str()
        self.d = dict()

    def parse_server_str(self, server_string):
        '''
        Parse the server string
        '''
        self.servstr = server_string.strip()[:-1]
        sslisted = self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w = i.split(' ')
            self.d[w[0]] = self.destringify(w[1:])

    def __repr__(self):
        out = str()
        for k in sorted(self.d):
            strout= str(self.d[k])
            if type(self.d[k]) is list:
                strlist= [str(i) for i in self.d[k]]
                strout= ', '.join(strlist)
            out+= "%s: %s\n" % (k,strout)
        return out
    
    def destringify(self, s):
        '''
        Converts a string into a value or a list of strings into a list of values (if possible)
        '''
        if not s: return s # if string is empty

        if type(s) is str:
            try:
                return float(s)
            except ValueError:
                print("Could not find a value in %s" % s)
                return s
        elif type(s) is list:
            if len(s) < 2:
                return self.destringify(s[0])
            else:
                return [self.destringify(i) for i in s]