import os

class Automator:
    def __init__(self, real = True):
        self.xdo_list = []
        self.real = real

    def xdo(self, xdo):
        self.xdo_list.append(xdo)

    def flush(self):
        if len(self.xdo_list) == 0: return

        command = '/usr/bin/xdotool' + ' '
        ctrl_idx = None
        for (idx, elem) in enumerate(self.xdo_list):
            if elem == "key ctrl+": ctrl_idx = idx
            if ctrl_idx is not None and idx == ctrl_idx+1: # we are after element "ctrl+"
                without_key = elem.replace('key ','')#we delete 'key '
                self.xdo_list[ctrl_idx] += without_key #we add the key to the element before us (ctrl+)
                self.xdo_list.pop(idx)#we remove this element
                break#we shortcircuit
        command += ' '.join(self.xdo_list)
        self.execute(command)
        self.xdo_list = []

    def execute(self, command):
        if command == '': return

        print "`%s`" % command
        if self.real:
            os.system(command)

    def raw_key(self, k):
        if(k == "'"): k = 'apostrophe'
        elif(k == '.'): k = 'period'
        elif(k == '-'): k = 'minus'
        self.xdo('key ' + k)
    def key(self, k):
        if(len(k) > 1): k = k.capitalize()
        self.xdo('key ' + k)
