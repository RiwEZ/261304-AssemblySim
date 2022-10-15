class Tokenizer():
    def __init__(self, lines: list[str]):
        self.lines = [l.strip() for l in lines if l.strip() != '']
        self.line = 0
        self.pos = 0
        self.next = ''
        self.compute_next()
    
    def get_info(self, w):
        if len(self.lines) == 0: return ''
        elif self.line < len(self.lines):
            info = self.lines[self.line]
            info = info.replace(w, '\x1b[0;37;41m' + w + '\x1b[0m', 1)

            return ':' + str(self.line + 1) + '\n\t' + info
        return ':unknown'

    def compute_next(self):
        if len(self.lines) == 0: return
        if self.line > len(self.lines) - 1:
            self.next = ''
            return

        curr_line = self.lines[self.line]
        self.next = ''

        while self.pos >= len(curr_line) or curr_line[self.pos].isspace():
            self.pos += 1
            if self.pos >= len(curr_line):
                if self.line == len(self.lines) - 1: return
                self.line += 1
                curr_line = self.lines[self.line]
                self.pos = 0
        
        while self.pos < len(curr_line) and curr_line[self.pos].isspace() == False:
            self.next += curr_line[self.pos]
            self.pos += 1

        return

    def has_next(self):
        return self.next != ''
    
    def peek(self):
        return self.next
    
    def consume(self):
        temp = self.next
        self.compute_next()
        return temp

    def consume_line(self):
        self.pos = 0
        self.line += 1
        self.compute_next()
    
 