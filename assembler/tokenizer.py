class Tokenizer():
    def __init__(self, lines: list[str]):
        self.lines = [l for l in lines if l != '']
        self.line = 0
        self.pos = 0
        self.next = ''
        self.compute_next()
    
    def get_info(self):
        if len(self.lines) == 0: return ''
        elif self.line < len(self.lines):
            return ':' + str(self.line) + '\n\t' + self.lines[self.line] + '\n\t' + (self.pos - 1) * ' ' + '^'
        return ':unknown'

    def compute_next(self):
        if len(self.lines) == 0: return
        if self.line > len(self.lines) - 1:
            self.next = ''
            return

        curr_line = self.lines[self.line]
        self.next = ''

        while self.pos >= len(curr_line) or curr_line[self.pos] == ' ':
            self.pos += 1
            if self.pos >= len(curr_line):
                if self.line == len(self.lines) - 1: return
                self.line += 1
                curr_line = self.lines[self.line]
                self.pos = 0
        
        while self.pos < len(curr_line) and curr_line[self.pos] != ' ':
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
    
 