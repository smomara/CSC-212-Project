class ParseNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        indent = "    " * level
        if not self.children:
            return f"{indent}[{self.name}]"
        elif isinstance(self.children, str):
            return f"{indent}[{self.name} {self.children}]"
        elif isinstance(self.children, ParseNode):
            return f"{indent}[{self.name}\n{self.children.__str__(level+1)}{indent}]"
        else:
            children_str = "\n".join(child.__str__(level+1) for child in self.children)
            return f"{indent}[{self.name}\n{children_str}\n{indent}]"

    def __repr__(self):
        return self._print_tree()

    def _print_tree(self, indent=0):
        result = " " * indent + str(self.name) + "\n"
        for child in self.children:
            result += child._print_tree(indent=indent + 2)
        return result

class Parser:
    def __init__(self, sentence):
        self.sentence = sentence
        self.index = 0
    
    def parse(self):
        tree = self.parse_s()
        #if self.index >= len(self.sentence):
        #    raise ValueError("Unexpected end of sentence")
        return tree
    
    def parse_s(self):
        np = self.parse_np()
        vp = self.parse_vp()
        return ParseNode('S', [np, vp])
    
    def parse_np(self):
        if self.match('D'):
            d = self.consume()
            if self.match('AJ'):
                aj = []
                while self.match('AJ'):
                    aj.append(self.consume())
                n = self.consume('N')
                return ParseNode('NP', [ParseNode('D', [ParseNode(d)])] +\
                                       [ParseNode('AJP', [ParseNode('AJ', [ParseNode(x)]) for x in aj] +\
                                                         [ParseNode('N', [ParseNode(n)])])])
            else:
                n = self.consume('N')
                return ParseNode('NP', [ParseNode('D', [ParseNode(d)]), ParseNode('N', [ParseNode(n)])])
        elif self.match('PN'):
            pn = self.consume()
            return ParseNode('NP', [ParseNode('PN', [ParseNode(pn)])])
        elif self.match('PPN'):
            ppn = self.consume()
            return ParseNode('NP', [ParseNode('PPN', [ParseNode(ppn)])])
        else:
            raise ValueError("Expected NP")
            
    def parse_vp(self):
        svp = self.parse_svp()
        try:
            if self.match('C'):
                c = self.consume()
                s = self.parse_s()
                return ParseNode('VP', [svp, ParseNode('C', [ParseNode(c)]), s])
            else:
                return ParseNode('VP', [svp])
        except:
            return ParseNode('VP', [svp])
    
    def parse_svp(self):
        preav = []
        while self.match('AV'):
            preav.append(self.consume())
            
        if self.match('IV'):
            iv = self.consume()
            
            aj = []
            if self.match('AJ'):
                aj.append(self.consume())
            
            postav = []
            while self.index < len(self.sentence) and self.match('AV'):
                postav.append(self.consume())
                
            return ParseNode('SVP', [ParseNode('AV', [ParseNode(x)]) for x in preav] + \
                                    [ParseNode('IV', [ParseNode(iv)])] +\
                                    [ParseNode('AJ', [ParseNode(x)]) for x in aj] +\
                                    [ParseNode('AV', [ParseNode(x)]) for x in postav])
        elif self.match('TV'):
            tv = self.consume()
            
            midav = []
            while self.index < len(self.sentence) and self.match('AV'):
                midav.append(self.consume())
            
            aj = []
            prepp = []
            np = []
            if self.index < len(self.sentence):
                if self.match('AJ'):
                    aj.append(self.parse_ajp())
                elif self.match('P'):
                    prepp.append(self.parse_pp())
                else:
                    try:
                        np.append(self.parse_np())
                    except:
                        pass
            
            postpp = []
            try:
                if self.match('P'):
                    postpp.append(self.parse_pp())
            except:
                pass
            
            postav = []
            while self.index < len(self.sentence) and self.match('AV'):
                    postav.append(self.consume())
            
            svp_node = ParseNode('SVP', [])
            for i in preav:
                svp_node.add_child(ParseNode('AV', [ParseNode(i)]))
            svp_node.add_child(ParseNode('TV', [ParseNode(tv)]))
            for i in midav:
                svp_node.add_child(ParseNode('AV', [ParseNode(i)]))
            for i in aj:
                svp_node.add_child(i)
            for i in prepp:
                svp_node.add_child(i)
            for i in np:
                svp_node.add_child(i)
            for i in postav:
                svp_node.add_child(ParseNode('AV', [ParseNode(i)]))
            for i in postpp:
                svp_node.add_child(i)
            return svp_node
    
    def parse_pp(self):
        if self.match('P'):
            p = self.consume('P')
            try:
                np = self.parse_np()
            except:
                raise ValueError('Expected NP')
            return ParseNode('PP', [ParseNode('P', [ParseNode(p)]), np])
        else:
            return None
    
    def parse_ajp(self):
        if self.match('AJ'):
            aj = []
            while self.index > len(self.sentence) and self.match('AJ'):
                aj.append(self.consume())
            try:
                np = self.parse_np()
            except:
                raise ValueError('Expected NP')
            return ParseNode('AJP', [ParseNode('AJ', [ParseNode(x)]) for x in aj] + np)
    
    def match(self, category):
        if self.index >= len(self.sentence):
            raise ValueError("Unexpected end of sentence")
        token = self.sentence[self.index]
        return token['category'] == category
    
    def consume(self, category = None):
        if self.index >= len(self.sentence):
            raise ValueError("Unexpected end of sentence")
        token = self.sentence[self.index]
        if category is not None and token['category'] != category:
            raise ValueError(f"Expected category {category} but found {token['category']}")
        self.index += 1
        return token['word']

# TODO: expand sets
# determiners
D_set = ('the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'its', 'our', 'their', 'any')

# prepositions
P_set = ('on', 'at', 'by', 'between', 'in', 'of', 'to', 'for', 'with', 'at', 'by', 'from', 'up')

# nouns
N_set = ('boy', 'competitor', 'boys', 'mom', 'moms', 'teacher', 'teachers', 'cat', 'cats', 'dog', 'dogs', 'tree', 'trees', 'car', 'cars', 'time', 'year', 'years', 'people', 'person', 'way', 'day', 'days', 'man', 'woman', 'men', 'women', 'thing', 'woman', 'life', 'child', 'children', 'world', 'school', 'state', 'family', 'student', 'students', 'group', 'country', 'problem', 'hand', 'part', 'place', 'case', 'week', 'company', 'system')

# pronouns
PN_set = ('I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves', 'mine', 'yours', 'his', 'hers', 'its')

# intransitive verbs
IV_set = ('be', 'is', 'was', 'have', 'had', 'has', 'do', 'did', 'say', 'said', 'go', 'went', 'get', 'got', 'make', 'made', 'know', 'knew', 'think', 'thought', 'see', 'saw', 'come', 'came', 'want', 'wanted', 'look', 'looked', 'use', 'used', 'find', 'found', 'give', 'gave', 'tell', 'told', 'work', 'worked', 'call', 'called', 'try', 'tried', 'feel', 'felt', 'become', 'became', 'leave', 'left', 'put', 'mean', 'meant')

# transitive verbs
TV_set = ('be', 'is', 'was', 'fail', 'looked', 'failed', 'seems', 'have', 'had', 'has', 'have', 'do', 'say', 'make', 'go', 'take', 'get', 'come', 'came', 'see', 'saw', 'know', 'knew', 'look', 'looked', 'want', 'wanted', 'give', 'gave', 'use', 'used', 'find', 'found', 'tell', 'told', 'ask', 'asked', 'work', 'worked', 'seem', 'seemed', 'feel', 'felt', 'try', 'studied', 'tried', 'leave', 'left', 'call', 'called', 'mean', 'meant', 'make', 'made', 'go', 'went', 'get', 'got', 'think', 'thought', 'look', 'want', 'give', 'gave', 'use', 'find', 'found', 'tell', 'ask', 'work', 'worked', 'seem', 'seemed', 'feel', 'felt', 'leave', 'left')

# adverbs
AV_set = ('hard', 'quickly', 'faster', 'slowly', 'well', 'poorly', 'yesterday', 'back', 'tomorrow', 'not', 'so', 'then', 'more', 'now', 'out', 'also', 'up', 'just', 'very', 'how', 'when', 'there', 'only', 'well', 'even', 'down', 'back', 'where', 'here', 'together', 'solo', 'alone')

# adjectives
AJ_set = ('independent', 'big', 'young', 'small', 'great', 'smart', 'dumb', 'young', 'two', 'scary', 'cute', 'other', 'new', 'good', 'high', 'old', 'great', 'big', 'American', 'small', 'large', 'national', 'young', 'different', 'black', 'long', 'little', 'important', 'political', 'bad', 'white', 'real', 'best', 'right', 'social', 'only', 'old', 'young', 'tall', 'short', 'skinny', 'fat', 'blonde', 'smart', 'dumb')

# conjunctions
C_set = ('and', 'or', 'but', 'so', 'yet', 'after', 'and', 'or', 'but', 'so', 'if', 'when', 'because', 'that', 'while', 'although')

import string

punctuations = set(string.punctuation)

sentence = str(input("Enter a sentence: "))

def tokenize(sentence):
    words = sentence.split()
    words = [w.strip(''.join(punctuations)).lower() for w in words]
    return words

def tag(words):
    tags = []
    for w in words:
        if w in D_set:
            tags.append('D')
        elif w in P_set:
            tags.append('P')
        elif w in C_set:
            tags.append('C')
        elif w in PN_set:
            tags.append('PN')
        elif w in TV_set:
            tags.append('TV')
        elif w in IV_set:
            tags.append('IV')
        elif w in AV_set:
            tags.append('AV')
        elif w in AJ_set:
            tags.append('AJ')
        elif w in N_set:
            tags.append('N')
        elif w in punctuations:
            continue
        else:
            tags.append('PPN')
    return tags

tokens = tokenize(sentence)
tags = tag(tokens)

parsed_sentence = [{'word': token, 'category': tag} for token, tag in zip(tokens, tags)]

parser = Parser(parsed_sentence)
tree = parser.parse()
print(tree)
