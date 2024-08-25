class DriverAction(object):
    '''What the driver is intending to do

    Composes something like this for the server:
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus 0)(meta 0) or
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus -90 -45 0 45 90)(meta 0)'''

    def __init__(self):
       self.actionstr = str()
       self.d = { 'accel':0.2,
                   'brake':0,
                  'clutch':0,
                    'gear':1,
                   'steer':0,
                   'focus':[-90,-45,0,45,90],
                    'meta':0
                    }


    def clip_to_limits(self):
        """There pretty much is never a reason to send the server
        something like (steer 9483.323). This comes up all the time
        and it's probably just more sensible to always clip it than to
        worry about when to. The "clip" command is still a snakeoil
        utility function, but it should be used only for non standard
        things or non obvious limits (limit the steering to the left,
        for example). For normal limits, simply don't worry about it."""

        self.d['steer'] = self.clip(self.d['steer'], -1, 1)
        self.d['brake'] = self.clip(self.d['brake'], 0, 1)
        self.d['accel'] = self.clip(self.d['accel'], 0, 1)
        self.d['clutch'] = self.clip(self.d['clutch'], 0, 1)

        if self.d['gear'] not in [-1, 0, 1, 2, 3, 4, 5, 6]:
            self.d['gear'] = 0
        if self.d['meta'] not in [0,1]:
            self.d['meta'] = 0
        if type(self.d['focus']) is not list or min(self.d['focus'])<-180 or max(self.d['focus'])>180:
            self.d['focus'] = 0
    
    def clip(self, v, lo, hi):
        '''Forces a value to fall between two bounds
        v = value
        lo = lower bound
        hi = higher bound'''
        if v < lo: return lo
        elif v > hi: return hi
        else: return v

    def __repr__(self):
        self.clip_to_limits()
        out = str()
        for k in self.d:
            out+= '('+k+' '
            v = self.d[k]
            if not type(v) is list:
                out += '%.3f' % v
            else:
                out += ' '.join([str(x) for x in v])
            out += ')'
        return out

